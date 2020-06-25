import os
import sys
import datetime
import time

from PIL import Image, ImageDraw

from life_game.Const import Const
from life_game.CellManager import CellManager


def out_gif_image(step_list):
    images = []
    black =(0,0,0)
    white = (0,255,0)
    width = Const.PIXEL_SIZE * Const.COLS
    height = Const.PIXEL_SIZE * Const.ROWS
    for step in step_list:
        _image = Image.new('RGB', (width,height), black)
        draw = ImageDraw.Draw(_image) 
        for cell in step['step']:
            fill = white if cell['status'] is Const.STATUS_ALIVE else (0,0,0)
            x = cell['x'] * Const.PIXEL_SIZE
            y = cell['y'] * Const.PIXEL_SIZE
            x2 = (cell['x']+1) * Const.PIXEL_SIZE
            y2 = (cell['y']+1) * Const.PIXEL_SIZE
            draw.rectangle([(x, y),( x2, y2)], fill=fill,outline=(0,0,0))

        images.append(_image)
    path = os.getcwd()
    dist_dir = path + '/dist'
    if not os.path.exists(dist_dir):
        os.mkdir(dist_dir)
    images[0].save(dist_dir+'/life_game_resurt_{}.gif'.format(int(datetime.datetime.now().timestamp() )),
        save_all=True, append_images=images[1:], optimize=False, duration=100, loop=0)


def main():
    start = datetime.datetime.now().timestamp()
    manager = CellManager(Const.COLS,Const.ROWS,Const.MAX_STEPS, Const.THRESHOLD)
    manager.create_cells(randomize=True)
    manager.run()
    out_gif_image(manager.history)
    end = datetime.datetime.now().timestamp()
    print('finish job {} seconds' .format(end - start))

if __name__ == '__main__':
    
    main()
