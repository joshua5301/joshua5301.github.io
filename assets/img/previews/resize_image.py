from PIL import Image

def resize_image(image_path: str, output_path: str, target_ratio: float, background_color: tuple[int, int, int, int]):
    """
    주어진 이미지를 새로운 비율로 된 배경의 중심에 붙여넣고 이를 PNG 파일로 저장합니다.

    Parameters
    ----------
    image_path : str
        원본 이미지의 경로
    output_path : str
        리사이징된 이미지를 저장할 경로
    target_ratio : float
        리사이징할 이미지의 가로:세로 비율
    background_color : tuple[int, int, int, int]
        리사이징된 이미지의 배경색 (RGBA)
    """

    image = Image.open(image_path)
    image = image.convert('RGBA')
    width, height = image.size
    target_width = max(width, int(height * target_ratio))
    target_height = max(height, int(width * (1 / target_ratio)))
    new_image = Image.new('RGBA', (target_width, target_height), background_color)
    paste_x = int((target_width - width) / 2)
    paste_y = int((target_height - height) / 2)
    new_image.paste(image, (paste_x, paste_y), mask=image.split()[3])
    new_image.save(output_path, 'png')


if __name__ == "__main__":
    """
    현재 디렉토리에 있는 모든 이미지를 리사이징하고 이를 resized 폴더에 저장합니다.
    """
    import os
    for file_name in os.listdir(os.path.dirname(os.path.abspath(__file__))):

        image_suffix = ['.png', '.jpg', '.jpeg']
        image_suffix = image_suffix + [s.upper() for s in image_suffix]
        if not file_name.endswith(tuple(image_suffix)):
            print('Skipping', file_name)
            continue

        image_name = file_name
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), image_name)
        output_name = image_name.split('.')[-2] + '.png'
        output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resized', output_name)
        target_ratio = 1.91  # 16:9
        background_color = (255, 255, 255, 255)  # 흰색
        resize_image(image_path, output_path, target_ratio, background_color)