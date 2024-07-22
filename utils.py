import math
import os
import cv2
import numpy as np
from scipy.interpolate import LinearNDInterpolator
import matplotlib.pyplot as plt

dimension = 100

def make_data():
    """
    Load light field images from the dataset and store them in a 4D numpy array.
    """
    image_path = "./dataset"
    files = os.listdir(image_path)
    files.sort()
    light_field_4d = np.zeros((17, 17, 1152, 1536, 3), dtype=np.uint8)
    
    for u in range(17):
        for v in range(17):
            print(f"{image_path}/{files[u * 17 + v]}")
            image = cv2.imread(f"{image_path}/{files[u * 17 + v]}")
            light_field_4d[u, v, :, :, :] = image
    
    return light_field_4d

def light_field_4d(s: float, t: float, u: float, v: float, data) -> set:
    """
    Interpolate the color values at the specified coordinates in the 4D light field data.
    """
    S = [math.floor(s), math.ceil(s), math.floor(s) - 1]
    T = [math.floor(t), math.ceil(t), math.ceil(t) + 1]
    U = [math.floor(u), math.ceil(u), math.floor(u) - 1]
    V = [math.floor(v), math.ceil(v), math.ceil(v) + 1]
    
    coords = []
    blue, green, red = [], [], []
    
    for s_coord in S:
        for t_coord in T:
            for u_coord in U:
                for v_coord in V:
                    coords.append((s_coord, t_coord, u_coord, v_coord))
                    if (
                        0 <= s_coord < 17
                        and 0 <= t_coord < 17
                        and 0 <= u_coord < 1152
                        and 0 <= v_coord < 1536
                    ):
                        blue.append(data[s_coord][t_coord][u_coord][v_coord][0])
                        green.append(data[s_coord][t_coord][u_coord][v_coord][1])
                        red.append(data[s_coord][t_coord][u_coord][v_coord][2])
                    else:
                        blue.append(0)
                        green.append(0)
                        red.append(0)
    
    blue_light_field = LinearNDInterpolator(coords, blue, 0)
    green_light_field = LinearNDInterpolator(coords, green, 0)
    red_light_field = LinearNDInterpolator(coords, red, 0)

    b = blue_light_field(s, t, u, v)
    g = green_light_field(s, t, u, v)
    r = red_light_field(s, t, u, v)

    return b, g, r

def light_field_renderer(x: float, y: float, z: float, theta: float, data, save_path) -> None:
    """
    Render an image from the 4D light field data based on given coordinates and angles.
    """
    image = np.zeros((dimension, dimension, 3))
    r = z / (1 - z)
    max_h = x + (1 - z) * math.tan(theta)
    min_h = x - (1 - z) * math.tan(theta)
    max_w = y + (1 - z) * math.tan(theta)
    min_w = y - (1 - z) * math.tan(theta)
    
    for h in range(dimension):
        for w in range(dimension):
            u = min_h + (max_h - min_h) * h / dimension
            v = min_w + (max_w - min_w) * w / dimension
            s = x + (x - u) * r
            t = y + (v - y) * r

            s *= 17
            t *= 17
            u *= 1152
            v *= 1536
            blue, green, red = light_field_4d(s, t, u, v, data)
            image[h, w, :] = [int(blue), int(green), int(red)]
    
    cv2.imwrite(save_path, image)

def light_field_renderer_rotate(omega, z, theta, data, save_path) -> None:
    """
    Render an image from the 4D light field data with rotation.
    """
    image = np.zeros((dimension, dimension, 3))
    r = z / (1 - z)

    x = 0.5 + 0.1 * math.sin(omega)
    y = 0.5 + 0.1 * math.cos(omega)
    phi_x = math.atan(0.1 * math.sin(omega) / (1 - z))
    phi_y = math.atan(0.1 * math.cos(omega) / (1 - z))
    max_h = x + (1 - z) * math.tan(theta + phi_x)
    min_h = x - (1 - z) * math.tan(theta - phi_x)
    max_w = y + (1 - z) * math.tan(theta + phi_y)
    min_w = y - (1 - z) * math.tan(theta - phi_y)
    
    for h in range(dimension):
        for w in range(dimension):
            u = min_h + (max_h - min_h) * h / dimension
            v = min_w + (max_w - min_w) * w / dimension
            s = x + (x - u) * r
            t = y + (v - y) * r

            s *= 17
            t *= 17
            u *= 1152
            v *= 1536
            blue, green, red = light_field_4d(s, t, u, v, data)
            image[h, w, :] = [int(blue), int(green), int(red)]
    
    cv2.imwrite(save_path, image)

def light_field_renderer_movable(
    x: float, y: float, z: float, theta: float, 
    camera_x: float, camera_y: float, camera_z: float, 
    data, save_path) -> None:
    """
    Render an image from the 4D light field data with a movable camera view.
    """
    image = np.zeros((dimension, dimension, 3))
    r = z / (1 - z)
    
    # Adjust for camera position
    x_rel = x - camera_x
    y_rel = y - camera_y
    z_rel = z - camera_z
    max_h = x_rel + (1 - z_rel) * math.tan(theta)
    min_h = x_rel - (1 - z_rel) * math.tan(theta)
    max_w = y_rel + (1 - z_rel) * math.tan(theta)
    min_w = y_rel - (1 - z_rel) * math.tan(theta)
    
    for h in range(dimension):
        for w in range(dimension):
            u = min_h + (max_h - min_h) * h / dimension
            v = min_w + (max_w - min_w) * w / dimension
            s = x_rel + (x_rel - u) * r
            t = y_rel + (v - y_rel) * r
            
            # Transform back to original coordinate system
            s += camera_x
            t += camera_y
            u += camera_x
            v += camera_y
            s *= 17
            t *= 17
            u *= 1152
            v *= 1536
            blue, green, red = light_field_4d(s, t, u, v, data)
            image[h, w, :] = [int(blue), int(green), int(red)]
    
    cv2.imwrite(save_path, image)