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
def jittering_cv(image, translation=5, scale=0.05):
    tx, ty = random.randint(-translation, translation), random.randint(-translation, translation)
    scale_factor = random.uniform(1 - scale, 1 + scale)
    M = np.float32([[scale_factor, 0, tx], [0, scale_factor, ty]])
    return cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))

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

        # 各変換を適用

        rotated_image_cv = rotate_cv(img_origin, random.randint(0, 360))
        adjusted_image_cv = adjust_brightness_contrast_cv(img_origin, alpha=random.uniform(0.7, 1.3), beta=random.randint(-50, 50))
        jittered_image_cv = jittering_cv(img_origin)

        # オリジナル画像とデータ拡張された画像を保存
        images_cv = [img_origin, rotated_image_cv, adjusted_image_cv, jittered_image_cv]
        suffixes = ["",  "_rotated", "_adjusted", "_jittered"]

        for img, suffix in zip(images_cv, suffixes):
            output_filepath = os.path.join(output_directory, os.path.splitext(filename)[0] + suffix + os.path.splitext(filename)[1])
            cv2.imwrite(output_filepath, img)

        print(f'Processed and saved: {filename}')