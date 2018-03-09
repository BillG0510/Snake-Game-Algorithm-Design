import sys
import math
import random
# Don't run into a player's light trail! Use your helper bots at strategic moments or as a last resort to be the last drone standing!

player_count = int(input())  # the number of at the start of this game
my_id = int(input())  # your bot's id

grid = [[0 for x in range(15)] for y in range(30)]
reach_map_ob = [[0 for x in range(15)] for y in range(30)]

ops = ["UP","RIGHT","DOWN","LEFT"]
#ops2 = ["RIGHT","DOWN","LEFT","UP"]
#ops3 = ["DOWN","LEFT","UP","RIGHT"]
#ops4 = ["LEFT","UP","RIGHT","DOWN"]
#ops = ops
def getNextPos(x,y,inp,i=1):
    reX = x
    reY = y
    #print(inp, file=sys.stderr)
    if inp=="UP":
        reY=y-i
        
    if inp=="DOWN":
        reY = y+i
        
    if inp=="RIGHT":
        reX=x+i
        
    if inp=="LEFT":
        reX=x-i
        
    if reY<-0:
        reY += 15 
    if reX<-0:
        reX += 30
    if reX>=30:
        reX -= 30
    if reY>=15:
        reY -= 15
    return reX,reY

def getNextPosInverse(x,y,now_x,now_y):
    #print(x, file=sys.stderr)
    #print(now_x, file=sys.stderr)
    if now_x!=x:
        if now_x==0 and x==29:
            return "RIGHT"
        if now_x==29 and x==0:
            return "LEFT"   
        if now_x>x:
            return "RIGHT"
        if now_x<x:
            return "LEFT"
        
    if now_y!=y:
        if now_y==0 and y==14:
            return "DOWN"
        if now_y==14 and x==0:
            return "UP" 
        if now_y>y:
            return "DOWN"
        if now_y<y:
            return "UP"
        
    return "UP"
    
def range2(x1,x2,k,Max):
    if x1<x2:
        return [x for x in range(x1,x2)]
    else:
        return [x for x in range(0,x2)]+[x for x in range(x1,Max)]

def get_map(x,y):
    reach_map = [[0 for x in range(15)] for y in range(30)]
    reach_map[x][y] = 1
    visited = [(x,y)]
    stack = []
    for o in ops:
        rX,rY = getNextPos(x,y,o,1)
        if (rX,rY) not in visited:
            stack.append((rX,rY))
    while stack:
        tx,ty = stack.pop()
        if grid[tx][ty]==0:
            reach_map[tx][ty]=1
            for o in ops:
                rX,rY = getNextPos(tx,ty,o,1)
                if (rX,rY) not in visited:
                    stack.append((rX,rY))
        visited.append((tx,ty))
        
        #print(stack, file=sys.stderr)
    return reach_map

def density(x,y,inp,k):
    counter =0
    tx=x
    ty=y
    #tx,ty = getNextPos(x,y,inp,1)
    _,dY = getNextPos(x,y,"DOWN",k)
    _,uY = getNextPos(x,y,"UP",k)
    rX,_ = getNextPos(x,y,"RIGHT",k)
    lX,_ = getNextPos(x,y,"LEFT",k)
    if inp=="DOWN":
        iter_X = range2(lX,rX+1,2*k,30)
        iter_Y = range2(ty,dY+1,k,15)
    if inp=="UP":
        iter_X = range2(lX,rX+1,2*k,30)
        iter_Y = range2(uY,ty+1,k,15)
    if inp=="LEFT":
        iter_X = range2(lX,tx+1,k,30)
        iter_Y = range2(uY,dY+1,2*k,15)
    if inp=="RIGHT":
        iter_X = range2(tx,rX+1,k,30)
        iter_Y = range2(uY,dY+1,2*k,15)
    print
    tx,ty = getNextPos(x,y,inp,1)
    reach_map = get_map(tx,ty)
    #print(k,file=sys.stderr)
    #print(iter_X,file=sys.stderr)
    #print(iter_Y,file=sys.stderr)
    for iX in iter_X:
        for iY in iter_Y:
            counter+=reach_map[iX][iY]
    return counter


def collision(x,y,inp):
    reX,reY = getNextPos(x,y,inp,1)
    #print(reX, file=sys.stderr)
    #print(reY, file=sys.stderr)
    #print(grid[reX][reY], file=sys.stderr)
    #print(reX,file=sys.stderr)
    #print(reY,file=sys.stderr)
    #print(grid[reX][reY],file=sys.stderr)
    if grid[reX][reY]!=0:
        return True
    else:
        return False

def headcollision(x,y,x_list,y_list,inp):
    reX,reY = getNextPos(x,y,inp,1)
    for ox,oy in zip(x_list,y_list):
        for o in ops:
            roX,roY = getNextPos(x,y,o,1)
            if roX==reX and roY==roY:
                return True
    return False
    
def killermode(x,y):
    tx,ty = getNextPos(x,y,inp,1)

def safemode(x,y):
    for o in ops:
        if not collision(x,y,o):
            return o
            
def inverse(op):
    if "UP":
        return "DOWN"
    if "LEFT":
        return "RIGHT"
    if "DOWN":
        return "UP"
    if "RIGHT":
        return "LEFT"
def getConnected(reachmap):
    counter = 0
    for x in range(30):
        for y in range(15):
            counter+=reachmap[x][y]
    return counter

def getDecision(x,y,x_list,y_list,remaining,direction):
    k_list = [6]
    r = []
    ok_ops = []
    coll_ops = []
    for o in ops:
        if not collision(x,y,o):
            #if headcollision(x,y,x_list,y_list,o):
            #r.append(o)
            #else:
            #print(o, file=sys.stderr)
            ok_ops.append(o)
            print("collision",file=sys.stderr)
            
        else:
            if o==direction:
                coll_ops.append(o)
    cc=0
    if remaining>0 and coll_ops:
        xx0,yy0 = getNextPos(x,y,direction,1)
        xx,yy = getNextPos(x,y,direction,2)
        if grid[xx][yy]==0 and (xx0,yy0) not in zip(x_list,y_list):
            coll_map = get_map(xx,yy)
            #print("collision ops",file=sys.stderr)
            cc = max(cc,getConnected(coll_map))
        xx2,yy2 = getNextPos(x,y,direction,3)
        if grid[xx2][yy2]==0 and (xx0,yy0) not in zip(x_list,y_list):
            if (grid[xx][yy]==1 and remaining>1) or grid[xx][yy]==0:
                coll_map = get_map(xx2,yy2)
            #print("collision ops",file=sys.stderr)
                cc = max(cc,getConnected(coll_map))
            
    for k in k_list:
        d_list = [density(x,y,o,k) for o in ok_ops]
        print(ok_ops,file=sys.stderr)
        print(d_list,file=sys.stderr)
        current_map = get_map(x,y)
        cn = getConnected(current_map)
        print(cn,file=sys.stderr)
        print(cc,file=sys.stderr)
        if cn<cc:
            return "DEPLOY"
        if ok_ops:
            op_max = ok_ops[0]
            d_max= d_list[0]
            for o,d in zip(ok_ops,d_list):
                if d_max<d:
                    d_max = d
                    op_max = o
        else:
            return "DEPLOY"
        #if coll_ops:
         #   if dc>d_max:
         #       return "DEPLOY"
        if d_max>0.1*2*k*k:
            return op_max
    return op_max
    #if r:
    #    return r
    #return "DEPLOY"
# game loop
conv = 0
direction = "UP"
oldx = 0
oldy = 0
#oplist = [ops1,ops2,ops3,ops4]
while True:
    my_x = 0
    my_y = 0
   
    
    x_list = []
    y_list = []
    #print(my_id, file=sys.stderr)
    helper_bots = int(input())  # your number of charges left to deploy helper bots
    for i in range(player_count):
        # x: your bot's coordinates on the grid (0,0) is top-left
        x, y = [int(j) for j in input().split()]
        #print(x,file=sys.stderr)
        #print(y,file=sys.stderr)
        grid[x][y] = 1
        if i==my_id:
            my_x = x
            my_y = y
        else:
            x_list.append(x)
            y_list.append(y)
    #reach_map = get_map(my_x,my_y)
    #print(my_x,file=sys.stderr)
    #print(my_y,file=sys.stderr)
    #print(reach_map,file=sys.stderr)
    #random.shuffle(ops)
    #print("coords",file=sys.stderr)
    #print(oldx,file=sys.stderr)
    #print(oldy,file=sys.stderr)
    #print(my_x,file=sys.stderr)
    #print(my_y,file=sys.stderr)
    direction = getNextPosInverse(oldx,oldy,my_x,my_y)
    print("direction",file=sys.stderr)
    print(direction,file=sys.stderr)
    oldx = my_x
    oldy = my_y
    #if conv>3:
    #    conv = 0
    #ops = oplist[conv]
    #conv+=1
    removal_count = int(input())  # the amount walls removed this turn by helper bots
    for i in range(removal_count):
        # remove_x: the coordinates of a wall removed this turn
        remove_x, remove_y = [int(j) for j in input().split()]
        grid[remove_x][remove_y] = 1
    
    #print(my_x,file=sys.stderr)
    #print(my_y,file=sys.stderr)
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)


    # DOWN | LEFT | RIGHT | UP or DEPLOY (to clear walls)
    operation = getDecision(my_x,my_y,x_list,y_list,helper_bots,direction)
    print(operation,file=sys.stderr)
    print(operation)