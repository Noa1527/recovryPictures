import os
import cv2
from PIL import Image
import numpy as np
import subprocess

def is_image_corrupted(image_path):
    try:
        with Image.open(image_path) as img:
            img.verify()
        return False
    except Exception as e:
        print(f"Erreur : {e}")
        return True

def read_image_from_sd_card(image_path):
    image = cv2.imread(image_path)
    return image

def display_image(image, window_name='Image'):
    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def is_image_file(file_name):
    lower_file_name = file_name.lower()
    return lower_file_name.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff'))

def restore_image(image):
    mask = np.all(image == (0, 0, 0), axis=-1)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    restored_image = cv2.inpaint(image, mask.astype(np.uint8), 3, cv2.INPAINT_NS)
    return restored_image

def recover_deleted_images(sd_card_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    photorec_executable = "./testdisk-7.2-WIP/photorec"  # Remplacez par le chemin réel de l'exécutable photorec
    command = [photorec_executable, "/d", output_folder, "/cmd", sd_card_path, "search"]
    subprocess.run(command)

def main():
    sd_card_path = "/Volumes/NO NAME"
    output_folder = "./RecoveredPictures"

    for file_name in os.listdir(sd_card_path):
        print(f"Traitement du fichier : {file_name}")
        if is_image_file(file_name):
            image_path = os.path.join(sd_card_path, file_name)

            if not is_image_corrupted(image_path):
                image = read_image_from_sd_card(image_path)
                display_image(image, window_name=f"Image: {file_name}")
            else:
                print(f"L'image {file_name} est corrompue.")
                image = read_image_from_sd_card(image_path)
                restored_image = restore_image(image)
                display_image(restored_image, window_name=f"Restored Image: {file_name}")

    recover_deleted_images(sd_card_path, output_folder)
    print(f"Les images supprimées ont été récupérées dans le dossier : {output_folder}")

if __name__ == '__main__':
    main()
