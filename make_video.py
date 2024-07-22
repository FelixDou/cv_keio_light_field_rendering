import cv2
import os


def create_video_from_images(image_folder, video_name, fps):
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    # Sort the images by number
    images.sort(key=lambda x: int(x.split("_")[-1].split(".")[0]))
    print(images)

    if not images:
        raise ValueError("No images found in the specified folder.")

    # Get the size of the images
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Use 'mp4v' for .mp4 format
    video = cv2.VideoWriter(video_name, fourcc, fps, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    image_folder = "./circle_view"
    video_name = "circle_video.mp4"
    fps = 10  # Frames per second

    create_video_from_images(image_folder, video_name, fps)
