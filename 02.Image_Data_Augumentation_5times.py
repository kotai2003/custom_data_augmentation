import cv2
import numpy as np
import random
import os

def get_scaled_pixel_color(image, scale_x, scale_y):
    """
    Returns the RGB color of the pixel at the scaled coordinates.

    :param image: Numpy array of the image.
    :param scale_x: Relative X-coordinate scale (0 to 1).
    :param scale_y: Relative Y-coordinate scale (0 to 1).
    :return: (R, G, B) tuple representing the color of the pixel.
    """
    # Calculate actual coordinates based on the image size and scale
    x = int(image.shape[1] * scale_x)
    y = int(image.shape[0] * scale_y)

    # Check if coordinates are within the image dimensions
    if x < 0 or y < 0 or x >= image.shape[1] or y >= image.shape[0]:
        raise ValueError("Calculated coordinates are outside the image bounds.")

    # Get the color (BGR format) and convert to RGB
    color_bgr = image[y, x]
    color_rgb = color_bgr[::-1]

    return tuple(color_rgb)


# ガウシアンノイズの追加
def add_noise_cv(image, noise_level=0.05):
    noise = np.random.normal(0, noise_level * 255, image.shape).astype(np.uint8)
    return cv2.add(image, noise)

# 回転（周辺は黒色）
def rotate_cv(image, angle):
    height, width = image.shape[:2]
    M = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
    return cv2.warpAffine(image, M, (width, height))

def rotate_cv2(image, angle, border_value):
    # Explicitly cast each element to int
    border_value = tuple(int(v) for v in border_value)

    # 画像の高さと幅を取得
    height, width = image.shape[:2]
    # 回転の中心を画像の中心に設定
    center = (width / 2, height / 2)

    # 回転に必要な行列を計算
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    # 回転を適用し、borderValueで指定された色で端を埋める
    rotated = cv2.warpAffine(image, M, (width, height), borderValue=border_value)

    return rotated


# 明るさとコントラストの調整
def adjust_brightness_contrast_cv(image, alpha=1.0, beta=0):
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

# ジッタリング（周辺は黒色）
def jittering_cv(image, translation=5, scale=0):
    tx, ty = random.randint(-translation, translation), random.randint(-translation, translation)
    scale_factor = random.uniform(1 - scale, 1 + scale)
    M = np.float32([[scale_factor, 0, tx], [0, scale_factor, ty]])
    return cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))

def process_image(image, filename, rotations_count=5, jitterings_count=5):
    # オリジナル画像を保存
    images_cv = [image]
    suffixes = [""]

    # # ノイズの追加と保存
    # noisy_image_cv = add_noise_cv(image, noise_level=0.01)
    # images_cv.append(noisy_image_cv)
    # suffixes.append("_noisy")

    # 明るさとコントラストの調整と保存
    # adjusted_image_cv = adjust_brightness_contrast_cv(image, alpha=random.uniform(0.7, 1.3), beta=random.randint(-50, 50))
    # images_cv.append(adjusted_image_cv)
    # suffixes.append("_adjusted")

    # 指定された回数の異なる回転と保存
    for i in range(rotations_count):
        pixel_result = get_scaled_pixel_color(image, scale_x=0.95, scale_y= 0.95)
        print(pixel_result)
        print(type(pixel_result))
        rotated_image_cv = rotate_cv2(image=image, angle=random.randint(-180, 180), border_value=pixel_result) #new function -180, 180
        images_cv.append(rotated_image_cv)
        suffixes.append(f"_rotated_{i}")

    # # 指定された回数の異なるジッタリングと保存
    # for i in range(jitterings_count):
    #     jittered_image_cv = jittering_cv(image,translation=20, scale=0)
    #     images_cv.append(jittered_image_cv)
    #     suffixes.append(f"_jittered_{i}")

    # すべての画像を保存
    for img, suffix in zip(images_cv, suffixes):
        output_filepath = os.path.join(output_directory, os.path.splitext(filename)[0] + suffix + os.path.splitext(filename)[1])
        cv2.imwrite(output_filepath, img)

if __name__ == '__main__':
    # 入力ディレクトリと出力ディレクトリ
    input_directory = './input_images'
    output_directory = './output_images'


    # 出力ディレクトリが存在しない場合は作成
    if not os.path.exists(output_directory):
        os.makedirs(output_directory, exist_ok=True)

    # 入力ディレクトリ内のすべての画像ファイルに対して処理
    for filename in os.listdir(input_directory):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            filepath = os.path.join(input_directory, filename)
            img_origin = cv2.imread(filepath)

            process_image(img_origin, filename, rotations_count=15, jitterings_count=0)  # ここで回転とジッタリングの回数を指定

            print(f'Processed and saved: {filename}')
