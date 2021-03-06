#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cv2 import aruco as aruco
import cv2
import numpy as np

DICT_44_250 = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)

#target markers will be from 0 to 9
MARKER_TARGET_RANGE = range(10)
#obstacle markers will be from 10 to 149
MARKER_OBSTACLE_RANGE = range(10, 150)
#other markers will be from 150 to 250
MARKER_OTHER =  range(150, 250)


def generate_markers(kind = 'target'):
    '''
    generate all markers for a given kind

    Parameters
    ----------
    kind : string, mandatory
        either 'target, 'obstacle', 'other'. The default is 'target'.

    Returns
    -------
    None.

    '''
    
    range_ = MARKER_TARGET_RANGE if kind == 'target' \
                else MARKER_OBSTACLE_RANGE if kind == 'obstacle' \
                else MARKER_OTHER

    margin = 50
    base = np.ones((200 + 2 * margin, 200 + 2 * margin), dtype=np.uint8) * 255
    
    #build the markers and save them to disk
    for idx in range_:
        curr_marker = aruco.drawMarker(dictionary=DICT_44_250, id=idx, sidePixels=200, borderBits=2)
        curr = base.copy()
        curr[margin:200+margin, margin:200+margin] = curr_marker
        cv2.imwrite(f'../data/markers/marker_{idx}.png', curr)
        
def generate_all_markers():
    generate_markers('target')
    generate_markers('obstacle')
    generate_markers('other')