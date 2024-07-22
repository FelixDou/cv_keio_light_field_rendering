from utils import (
    make_data,
    light_field_renderer,
    light_field_renderer_rotate,
    light_field_renderer_movable,
)
import math

def main():
    """
    Main function to load data and generate images.
    """
    data = make_data()
    print("Data loaded!")

    save_images(data)
    rotate_samples(data)
    generate_movable_view_sequence(data)

def save_images(data):
    """
    Generates and saves a series of images with varying depth (z-axis).
    """
    for z in range(-5, 6):
        light_field_renderer(0.5, 0.5, z * 0.1, 0.5, data, f"./video_image/{z+5}.png")
    print("Images saved!")

def rotate_samples(data):
    """
    Generates and saves a series of images with varying rotation angles.
    """
    for i in range(20):
        light_field_renderer_rotate(0.3 * i, 0.3, 0.5, data, f"./rotate_sample/{i}.png")
    print("Rotation samples saved!")

def generate_movable_view_sequence(data):
    """
    Generates a sequence of images with a moving point of view, rotation, and zoom.
    """
    num_frames = 100
    radius = 0.5
    center_x, center_y, center_z = 0.5, 0.5, 0.5
    zoom_range = (0.3, 0.7)

    for i in range(num_frames):
        # Calculate camera position for rotation
        angle = 2 * math.pi * i / num_frames
        camera_x = center_x + radius * math.cos(angle)
        camera_y = center_y + radius * math.sin(angle)

        # Calculate zoom factor (oscillating between zoom_range)
        zoom_factor = zoom_range[0] + (zoom_range[1] - zoom_range[0]) * (
            0.5 + 0.5 * math.sin(4 * math.pi * i / num_frames)
        )
        camera_z = center_z + zoom_factor

        # Adjust theta (field of view) based on zoom
        theta = 0.5 * (
            1 - (zoom_factor - zoom_range[0]) / (zoom_range[1] - zoom_range[0])
        )

        # Render and save the image for the current frame
        light_field_renderer_movable(
            center_x,
            center_y,
            center_z,
            theta,
            camera_x,
            camera_y,
            camera_z,
            data,
            f"./circle_view/{i:03d}.png",
        )
        print(f"Movable view image {i} saved!")

if __name__ == "__main__":
    main()