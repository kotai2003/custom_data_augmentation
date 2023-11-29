import cv2
import numpy as np
import random
import os


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
    adjusted_image_cv = adjust_brightness_contrast_cv(image, alpha=random.uniform(0.7, 1.3), beta=random.randint(-50, 50))
    images_cv.append(adjusted_image_cv)
    suffixes.append("_adjusted")

    # 指定された回数の異なる回転と保存
    for i in range(rotations_count):
        rotated_image_cv = rotate_cv(image, random.randint(-10, 10))
        images_cv.append(rotated_image_cv)
        suffixes.append(f"_rotated_{i}")

    # 指定された回数の異なるジッタリングと保存
    for i in range(jitterings_count):
        jittered_image_cv = jittering_cv(image,translation=20, scale=0)
        images_cv.append(jittered_image_cv)
        suffixes.append(f"_jittered_{i}")

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

            process_image(img_origin, filename, rotations_count=5, jitterings_count=5)  # ここで回転とジッタリングの回数を指定

            print(f'Processed and saved: {filename}')
