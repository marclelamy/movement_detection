# Control webcam and take photos
import cv2

# Open image and compare them
from PIL import Image, ImageOps

# To become Dr Strange
import time
from datetime import datetime


def image_similarity(image1, image2, mirror=True):
    """Compare two images and return a float indicating a similarity score 
    between 0 and 100 where 100 means both images are identicals. 
    Takes two arguments, photo paths.
    If mirror is True, it will mirror the image."""
    i1 = Image.open(image1)
    m1 = ImageOps.mirror(i1)
    i2 = Image.open(image2)

    if i1.size != i2.size:
        return 0

    results = []
    photos = [i1] if mirror == False else [i1, m1]
    
    for img1 in photos:
        pairs = zip(img1.getdata(), i2.getdata())
        if len(img1.getbands()) == 1:
            # for gray-scale jpegs
            dif = sum(abs(p1-p2) for p1,p2 in pairs)
        else:
            dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))

        ncomponents = img1.size[0] * img1.size[1] * 3
        
        results.append(round(100 - (dif / 255.0 * 100 / ncomponents), 2))
    
    
    return max(results)





if __name__ == '__main__':
    # initialize the camera
    camera = cv2.VideoCapture(0)

    # Saves an initial image
    return_value, image = camera.read()
    cv2.imwrite(f'last_image.png', image)

    # Defining images paths
    last_img_path = "last_image.png"
    new_img_path = "new_image.png"

    time_sleep = 0
    while True:
        # Saves new image
        return_value, image = camera.read()
        cv2.imwrite(new_img_path, image)

        # Compare both images
        similarity_score = image_similarity(last_img_path, new_img_path)

        # Check if the images are not similar, if true, writes the image in a folder
        if similarity_score < 95:
            time_now = str(datetime.now()).split(" ")[1].split(".")[0]
            cv2.imwrite(f"saved_photos/{time_now}_{new_img_path}", image)

        else: 
            time.sleep(time_sleep)


        print(similarity_score, end="\r")

        # Replace the last by the new image
        cv2.imwrite(last_img_path, image)


        