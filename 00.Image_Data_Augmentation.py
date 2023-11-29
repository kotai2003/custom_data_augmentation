import cv2
import numpy as np
import random
import matplotlib.pyplot as plt

# ガウシアンノイズの追加
def add_noise_cv(image, noise_level=0.05):
    noise = np.random.normal(0, noise_level * 255, image.shape).astype(np.uint8)
    return cv2.add(image, noise)

# 回転（周辺は黒色）
def rotate_cv(image, angle):
    height, width = image.shape[:2]
    M = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
    return cv2.warpAffine(image, M, (width, height))

# 明るさとコントラストの調整
def adjust_brightness_contrast_cv(image, alpha=1.0, beta=0):
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

# ジッタリング（周辺は黒色）
def jittering_cv(image, translation=5, scale=0.05):
    tx, ty = random.randint(-translation, translation), random.randint(-translation, translation)
    scale_factor = random.uniform(1 - scale, 1 + scale)
    M = np.float32([[scale_factor, 0, tx], [0, scale_factor, ty]])
    return cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    img_origin = cv2.imread('./images/01_surface-normal-img-2023-07-26-17-36-48-.png')

    # 各変換を適用
    noisy_image_cv = add_noise_cv(img_origin, noise_level=0.002)
    rotated_image_cv = rotate_cv(img_origin, random.randint(0, 360))
    adjusted_image_cv = adjust_brightness_contrast_cv(img_origin, alpha=random.uniform(0.7, 1.3), beta=random.randint(-50, 50))
    jittered_image_cv = jittering_cv(img_origin)

    # 結果を表示
    images_cv = [img_origin, noisy_image_cv, rotated_image_cv, adjusted_image_cv, jittered_image_cv]
    titles_cv = ["Original", "Noisy", "Rotated", "Adjusted", "Jittered"]

    for img, title in zip(images_cv, titles_cv):
        cv2.imshow(title, img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()






