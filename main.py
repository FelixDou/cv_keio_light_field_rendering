from utils import (
    make_bulldozer_data,
    bulldozer_light_field_renderer_movable,
    bulldozer_light_field_renderer,
    bulldozer_light_field_renderer_rotate,
)
import math

rectified_data = make_bulldozer_data()
print("Finished Load Data!")

for z in range(-5, 6):
    bulldozer_light_field_renderer(
        0.5,
        0.5,
        z * 0.1,
        0.5,
        rectified_data,
        f"./video_image/{z+5}.png",
    )
    print("image saved!")

# for i in range(20):
#     bulldozer_light_field_renderer_rotate(
#         0.3 * i, 0.3, 0.5, rectified_data, f"./rotate_sample/{i}.png"
#     )


# def generate_movable_view_sequence(data):
#     # Generate a sequence of images with moving point of view, rotation, and zoom
#     num_frames = 100
#     radius = 0.5
#     center_x, center_y, center_z = 0.5, 0.5, 0.5
#     zoom_range = (0.3, 0.7)  # Min and max zoom levels

#     for i in range(num_frames):
#         # Calculate camera position for rotation
#         angle = 2 * math.pi * i / num_frames
#         camera_x = center_x + radius * math.cos(angle)
#         camera_y = center_y + radius * math.sin(angle)

#         # Calculate zoom factor (oscillating between zoom_range)
#         zoom_factor = zoom_range[0] + (zoom_range[1] - zoom_range[0]) * (
#             0.5 + 0.5 * math.sin(4 * math.pi * i / num_frames)
#         )
#         camera_z = center_z + zoom_factor

#         # Adjust theta (field of view) based on zoom
#         theta = 0.5 * (
#             1 - (zoom_factor - zoom_range[0]) / (zoom_range[1] - zoom_range[0])
#         )

#         bulldozer_light_field_renderer_movable(
#             center_x,
#             center_y,
#             center_z,
#             theta,
#             camera_x,
#             camera_y,
#             camera_z,
#             data,
#             f"./circle_view/{i:03d}.png",
#         )
#         print(f"Movable view image {i} saved!")


generate_movable_view_sequence(rectified_data)
