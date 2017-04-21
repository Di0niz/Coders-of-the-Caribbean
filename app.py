# -*- coding: utf-8 -*-
import sys
import math


# convert cube to odd-r offset
def cube_to_offset(cube):
    x, y, z = cube

    col = x + (z - (z&1)) / 2
    row = z
    return (col, row)

# convert odd-r offset to cube
def offset_to_cube(offset):
    col,row = offset

    x = col - (row - (row&1)) / 2
    z = row
    y = -x-z
    return (x,y,z)

def cube_distance(a, b):
    ax, ay, az = a
    bx, by, bz = b

    return (abs(ax - bx) + abs(ay - by) + abs(az - bz)) / 2

def cube_direction(rotation):
    directions = [
        ( 1,-1, 0), ( 1, 0,-1), (0, 1,-1),
        (-1, 1, 0), (-1, 0, 1), (0,-1, 1)
    ]
    return directions[rotation]

def cube_add(a, b):
    ax, ay, az = a
    bx, by, bz = b

    return (ax + bx, ay + by, az + bz)

def cube_scale(hex, radius):
    x, y, z = hex
    return (x * radius, y * radius, z * radius)

def cube_neighbor(hex, rotation, radius = 1):
        return cube_add(hex, cube_scale(cube_direction(rotation), radius))

def cube_rotation(a, b):
    ax, ay, az = a
    bx, by, bz = cube_near(a, b)

    x, y, z = (bx - ax, by - ay, bz - az)
    
    #print >> sys.stderr, (bx, by, bz), a, " = ",  (x, y, z)
    rotation = -1
    for i in range(6):

        dx, dy, dz = cube_direction(i)

        if dx == x and dy == y and dz == z:
            rotation = i
            break

    return rotation

def cube_round(hex):
    hx, hy, hz = hex
    rx, ry, rz = int(hx), int(hy), int(hz)
    diff_x, diff_y, diff_z = abs(rx-hx),abs(ry-hy), abs(rz-hz)

    if diff_x > diff_y and diff_x > diff_z:
        rx = -ry-rz
    elif diff_y > diff_z:
        ry = -rx-rz
    else:
        rz = -rx-ry

    return (rx,ry,rz)

def lerp(a, b, t): 
    return a + (b - a) * t

def cube_lerp(a, b, t): 
    ax, ay, az = a
    bx, by, bz = b
    return (lerp(ax, bx, t), 
            lerp(ay, by, t),
            lerp(az, bz, t))


def cube_near(a, b):
    N = cube_distance(a, b)
    return cube_round(cube_lerp(a, b, 1.0/N ))



class EntityType(object):
    """Описание внутриигровых объектов"""
    SHIP, BARREL, MINE, CANNONBALL = "SHIP", "BARREL", "MINE", "CANNONBALL"


class Entity(object):
    """Определение базового класса внутриигровых объектов"""
    def __init__(self, entity_id, x, y):
        self.entity_id = entity_id
        self.x, self.y = x, y

    def update(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return "%d" % self.entity_id

    def dist_to(self, to_unit):
        return self.dist_to_target((to_unit.x, to_unit.y))

    def dist_to_target(self, target):
        self_cube = offset_to_cube((self.x, self.y))
        unit_cube = offset_to_cube(target)
        return cube_distance(self_cube, unit_cube)

    def rotation_to(self, to_unit):
        return self.rotation_to_target((to_unit.x, to_unit.y))

    def rotation_to_target(self, target):

        ship_cube = offset_to_cube((self.x, self.y))
        target_cube = offset_to_cube(target)

        return cube_rotation(ship_cube, target_cube)

class ShipEntity(Entity):
    def __init__(self, entity_id, x, y, rotation, speed, rum, player):
        Entity.__init__(self, entity_id, x, y)
        self.speed = speed
        self.rum = rum
        self.rotation = rotation
        self.player = player
        self.fire_wait = 0
        # перечисление точек, в которых находится 
        self.collitions = []

    def update(self, x, y, rotation, speed, rum, player):
        Entity.update(self, x, y)
        self.speed = speed
        self.rum = rum
        self.rotation = rotation
        self.player = player
        self.fire_wait = max(0, self.fire_wait -1)

    def find_near_entity(self, entities):
        near_entity = None
        min_dist = 10000

        for entity in entities:
            cur_dist = self.dist_to(entity)

            if cur_dist < min_dist:
                near_entity = entity
                min_dist = cur_dist

        return near_entity
        
    def can_move(self, world):
        
        cur_speed = min(1, self.speed) + 1
        current_point = offset_to_cube((self.x,self.y))
        next_point = cube_neighbor(current_point, self.rotation, cur_speed)

        x,y = cube_to_offset(next_point)

        return (0< x < 22) and (0 < y < 20)

    def make_command(self, command):
        if command[0] == Commands.MOVE:
            res = "MOVE %d %d" % (command[1].x, command[1].y)
        elif command[0] == Commands.FIRE:
            res = "FIRE %d %d" % (command[1].x, command[1].y)
            self.fire_wait = 2
        elif command[0] == Commands.WAIT:
            res = "WAIT"
        elif command[0] == Commands.STARBOARD:
            res = "STARBOARD"
        elif command[0] == Commands.PORT:
            res = "PORT"
        elif command[0] == Commands.FASTER:
            res = "FASTER"
        elif command[0] == Commands.SLOWER:
            res = "SLOWER"
        return res

    def future(self, command):

        # расчитываем новую скорость
        if command == Commands.FASTER:
            speed = min(2, self.speed + 1)
        elif command == Commands.SLOWER:
            speed = max(0, self.speed - 1)
        else:
            speed = self.speed

        hex = offset_to_cube((self.x, self.y))

        new_pos = cube_neighbor(hex, self.rotation, speed)
        front = cube_neighbor(new_pos, self.rotation, -1)
        back = cube_neighbor(new_pos, self.rotation, 1)

        newx, newy = cube_to_offset(new_pos)

        if command == Commands.PORT:
            rotation = (self.rotation + 1)% 6
        elif command == Commands.STARBOARD:
            rotation = (self.rotation + 5)% 6
        else:
            rotation = self.rotation

        if not (0 <= newx < 23):
            return None

        if not (0 <= newy < 21):
            return None


        new_ship = ShipEntity(self.entity_id, newx, newy, rotation, speed, self.rum-1, self.player)

        # сначала запоминаем обычную позицию
        new_ship.collitions = [cube_to_offset(back), cube_to_offset(new_pos), cube_to_offset(front)]


        # потом добавляем результат поворота
        if rotation != self.rotation:
            front = cube_neighbor(new_pos, new_ship.rotation, -1)
            back = cube_neighbor(new_pos, new_ship.rotation, 1)

            new_ship.collitions.append(cube_to_offset(back))
            new_ship.collitions.append(cube_to_offset(front))

        return new_ship

    def futures(self):
        if self.rum == 0:
            return []

        commands = [Commands.FASTER, Commands.PORT, Commands.STARBOARD, Commands.SLOWER, Commands.WAIT]
        futures = []
        for com in commands:
            f_ship = self.future(com)
            if f_ship is not None:
                futures.append(f_ship)
        return futures
        

    def __repr__(self):
        return "S%d [%d,%d]" % (self.entity_id, self.x,self.y)

class BarrelEntity(Entity):
    def __init__(self, entity_id, x, y, rum):
        Entity.__init__(self, entity_id, x, y)
        self.rum = rum

    def __repr__(self):
        return "B%d" % self.entity_id

class CannonballEntity(Entity):
    def __init__(self, entity_id, x, y, target, remain_turns):
        Entity.__init__(self, entity_id, x, y)
        self.target = target
        self.remain_turns = remain_turns

    def __repr__(self):
        return "B%d" % self.entity_id

class MineEntity(Entity):
    def __init__(self, entity_id, x, y):
        Entity.__init__(self, entity_id, x, y)
        #self.rum = rum

    def __repr__(self):
        return "M%d" % self.entity_id

class World(object):
    """Описание игрового мира"""

    WIDTH = 23
    HEIGHT = 21

    def __init__(self):
        """ Определяем список объектов доступных для класса """
        self.allships = {}

    def update(self):

        self.ships = []
        self.barrels = []
        self.enemyships = []
        self.cannonballs = []
        self.mines = []

        # инициализируем поле
        self.field = {}

        my_ship_count = int(raw_input())  # the number of remaining ships
        print >> sys.stderr, my_ship_count

        entity_count = int(raw_input())  # the number of entities (e.g. ships, mines or cannonballs)
        print >> sys.stderr, entity_count
        for i in xrange(entity_count):

            raw = raw_input()
            print >> sys.stderr, raw
            entity_id, entity_type, x, y, arg_1, arg_2, arg_3, arg_4 = raw.split()
            if entity_type == EntityType.BARREL:
                barrel = BarrelEntity(int(entity_id), int(x), int(y), int(arg_1))
                self.barrels.append(barrel)
                self.field[(int(x), int(y))] = barrel
            elif entity_type == EntityType.CANNONBALL:
                cannonball = CannonballEntity(int(entity_id), int(x), int(y), int(arg_1), int(arg_2))
                #self.field[(int(x), int(y))] = int(arg_2)
            elif entity_type == EntityType.MINE:

                mine = MineEntity(int(entity_id), int(x), int(y))
                self.mines.append(mine)
                self.field[(int(x), int(y))] = mine
            
            elif entity_type == EntityType.SHIP:

                if not int(entity_id) in self.allships:
                    ship = ShipEntity(int(entity_id), int(x), int(y), int(arg_1), int(arg_2), int(arg_3), int(arg_4))
                    # сохраняем информацию о корабле
                    self.allships[int(entity_id)] = ship
                else:
                    ship = self.allships[int(entity_id)]
                    ship.update(int(x), int(y), int(arg_1), int(arg_2), int(arg_3), int(arg_4))

                if arg_4 == "1":
                    self.ships.append(ship)
                else:
                    self.enemyships.append(ship)

                # устанавливаем центр
                self.field[(int(x), int(y))] = 0

    def collision(self, ship):
        """Проверяем пересечение коробля с минами"""

        hex = offset_to_cube((ship.x, ship.y))
        col = False
        for i in range(3, ship.speed *2 + 1):

            neighbor = cube_to_offset(cube_neighbor(hex, ship.rotation, i))

            if neighbor in self.field:
                target = self.field[neighbor]
                if isinstance(target,MineEntity):
                    col = True

        return col

    def find_short_path(self, ship, goals):
        """описываем алгоритм поиска корабля

        За основу взят алгоритм с wiki
        https://en.wikipedia.org/wiki/Dijkstra's_algorithm
        """

        node = start.x, start
        frontier = [node]
        explored = []

        # определение оптимальных вершин
        vertex = {node:(0, None)}

        # пока есть что обходить
        while not (node is None or len(frontier) == 0):

            node = frontier.pop()

            explored.append(node)

            distance = vertex[node][0]

            for n in self.get_nodes(node):
                if n not in explored:

                    # определяем дистанцию по количеству ходов до точке
                    next_distance = distance + self.links[node.entity_id][n.entity_id]

                    # помечаем текущую вершину
                    if n not in vertex or next_distance < vertex[n][0]:
                        vertex[n] = (next_distance, node)

                    if not (n in frontier or n in goals):
                        frontier.append(n)

        return vertex


    def find_shortest(self, start, goals):
        """Описание алгоритма поиска кратчайшего пути"""
        vertex = self.uniform_cost_search(start, goals)
        # востанавливаем цепочку

        min_len = 10
        min_solution = []
        for goal in goals:
            solution = [goal]
            node = vertex[goal][1]
 
            while node is not None:
                solution.insert(0, node)
                node = vertex[node][1]

            if min_len > len(solution):
                min_solution = solution

        return solution


    def get_nodes(self, node):
        """Определение списка соседних вершин"""

        i = node.entity_id

        nodes = []
        for j in xrange(self.num_factory):
            newnode = self.factories[j]
            if self.links[i][j] > 0 and i != j and newnode not in nodes:
                nodes.append(newnode)

        return nodes


        


class Commands(object):
    MOVE = 1
    FIRE = 2
    MINE = 3
    SLOWER = 4
    WAIT = 5
    PORT = 6
    STARBOARD = 7
    FASTER = 8
    SLOWER = 9

class Actions(object):
    MOVE = "MOVE"
    FIRE = "FIRE"
    FIRE_ENEMY = "FIRE_ENEMY"
    NEAR_ENEMY = "NEAR_ENEMY"
    NEED_RUM = "NEED_RUM"
    MOVE_ENEMY = "MOVE_ENEMY"
    MOVE_RUM = "MOVE_RUM"
    MOVE_RING = "MOVE_RING"
    MOVE_PORT = "MOVE_PORT"
    MOVE_STARBOARD = "MOVE_STARBOARD"
    MOVE_FASTER = "MOVE_FASTER"
    MOVE_SLOWER = "MOVE_SLOWER"
    EXCLUDE_MINE = "EXCLUDE_MINE"

class Problems(object):
    MOVE = 1

def SUB(l, exclude = None):
    if not exclude is None:
        return [x for x in l if x!=exclude]
    return l
    
class Strategy(object):

    def __init__(self, world):
        self.world = world

    def find_problem(self, ship, near_enemy, near_barrel):

        action = Actions.MOVE

        if self.world.collision(ship):
            action = Actions.EXCLUDE_MINE
        elif ship.rum > 70:
            action = Actions.MOVE_ENEMY
        elif near_enemy.speed == 0 and ship.dist_to(near_enemy) < 3:
            action = Actions.MOVE_ENEMY
        else:
            action = Actions.NEED_RUM

        return action

    def get_actions(self, ship, exclude = None):

        print >> sys.stderr, ship

        command = None
        action = None

        near_enemy = ship.find_near_entity(SUB(self.world.enemyships, exclude))
        near_barrel = ship.find_near_entity(SUB(self.world.barrels, exclude))

        action = self.find_problem(ship, near_enemy, near_barrel)

        target = 0

        while command is None:

            if action == Actions.MOVE:

                # проверяем препятствие

                # определяем разворот
                rotation = ship.rotation_to_target(target)

                d_rot = (rotation - ship.rotation + 6) % 6

                if d_rot == 0 and ship.speed == 0:
                    action = Actions.MOVE_FASTER
                elif d_rot == 0 and ship.speed == 1 and ship.dist_to_target(target) > 3:
                    action = Actions.MOVE_FASTER
                elif d_rot == 0 and ship.speed == 2:
                    action = Actions.FIRE_ENEMY
                elif d_rot < 3:
                    if ship.speed == 2 and ship.dist_to_target(target) < 3:
                        action = Actions.MOVE_SLOWER
                    else:
                        action = Actions.MOVE_PORT
                elif d_rot > 3:
                    if ship.speed == 2 and ship.dist_to_target(target) < 3:
                        action = Actions.MOVE_SLOWER
                    else:
                        action = Actions.MOVE_STARBOARD
                else:
                    action = Actions.FIRE_ENEMY

            elif action == Actions.MOVE_ENEMY:

                if near_enemy.speed > 0 and ship.dist_to(near_enemy) > 3:
                    action = Actions.MOVE
                    target = near_enemy.x, near_enemy.y
                elif near_enemy.speed == 0:
                    action = Actions.FIRE
                else:
                    command = (Commands.WAIT, )

            elif action == Actions.EXCLUDE_MINE:
                if ship.speed == 2:
                    action = Actions.MOVE_SLOWER
                else:
                    action = Actions.MOVE_PORT

            elif action == Actions.NEED_RUM:
                if near_barrel is None:
                    action = Actions.MOVE_ENEMY
                else:
                    action = Actions.MOVE
                    target = near_barrel.x, near_barrel.y

            elif action == Actions.FIRE_ENEMY:
                if ship.fire_wait == 0:
                    command = (Commands.FIRE, near_enemy)
                else:
                    command = (Commands.WAIT, None)
            elif action == Actions.FIRE:
                
                if ship.fire_wait == 0:
                    action = Actions.FIRE_ENEMY
                elif ship.dist_to(near_enemy) < 3:
                    action = Actions.MOVE_RING
                else:
                    action = Actions.MOVE
                    target = (near_enemy.x,near_enemy.y)

            elif action == Actions.MOVE_RING:
                
                ship_cube = offset_to_cube((ship.x, ship.y))

                enemy_cube = offset_to_cube((near_enemy.x, near_enemy.y))
                #определяем разворот
                rotation = cube_rotation(ship_cube, enemy_cube)
                rotation = (rotation + 1) % 6
                # поворачиваем
                next_cube = cube_neighbor(ship_cube, rotation)

                target = cube_to_offset(next_cube)
                action = Actions.MOVE

            elif action == Actions.MOVE_PORT:
                command = (Commands.PORT, None)
            elif action == Actions.MOVE_STARBOARD:
                command = (Commands.STARBOARD, None)
            elif action == Actions.MOVE_FASTER:
                command = (Commands.FASTER, None)

            elif action == Actions.MOVE_SLOWER:
                command = (Commands.SLOWER, None)




            print >> sys.stderr, action, command


        return command


WORLD = World()

while False:

    WORLD.update()

    STRATEGY = Strategy(WORLD)

    commands = {}

    for my_ship in WORLD.ships:
        commands[my_ship] = STRATEGY.get_actions(my_ship)

    # проверяем есть ли дубли, если есть тогда исключаем общую цель
#    for i in WORLD.ships:
#        for j in WORLD.ships:
#            if i != j:
#                if commands[i][0] == Commands.MOVE and isinstance(commands[i][1],BarrelEntity):
#                    if commands[i][1] == commands[j][1]:
#                        commands[j] = STRATEGY.get_actions(j, commands[j][1])
    
    # выводим список доступных комманд
    # сохраняем порядок работы с короблем
    for ship in WORLD.ships:
        command = ship.make_command(commands[ship])
        print command
