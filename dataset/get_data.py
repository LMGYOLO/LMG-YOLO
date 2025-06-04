import os
import shutil
import threading
import xml.etree.ElementTree as ET

# 定义需要的类别
valid_categories = ['defect', 'dent', 'dirty', 'flip', 'guangmian', 'gumming', 'pianmamian', 'scratch', 'dirt', 'filp', 'Gumming']

# 复制文件的函数
def copy_file(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)
    shutil.copy(src, dst)
    print(f'已复制文件: {src} 到 {dst}')


# 获取文件夹下所有图像文件和对应的xml文件
def get_image_and_xml_files(src_folder):
    image_files = []
    xml_files = []

    for root, dirs, files in os.walk(src_folder):
        for file in files:
            # 判断文件是否是图像文件
            if file.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
                image_path = os.path.join(root, file)
                # 生成对应的xml文件路径
                xml_path = os.path.join(root, file.replace(file.split('.')[-1], 'xml'))

                # 检查对应的xml文件是否存在
                if os.path.exists(xml_path):
                    # 解析xml文件
                    tree = ET.parse(xml_path)
                    root_element = tree.getroot()

                    # 假设类别信息在XML的特定标签内（如 <object><name>...<name></object>）
                    # 根据实际XML结构调整这里的解析
                    category_elements = root_element.findall('.//name')  # 假设类别在 <name> 标签下

                    valid = True  # 用于标记XML是否有效

                    # 遍历所有类别并检查是否符合要求
                    for category in category_elements:
                        category_name = category.text  # 获取类别并转为小写

                        # 如果类别不在有效列表中，则跳过该XML文件
                        if category_name not in valid_categories:
                            valid = False
                            break

                        # 替换类别名称
                        if category_name == 'filp':
                            category.text = 'flip'
                        elif category_name == 'dirt':
                            category.text = 'dirty'
                        elif category_name == 'Gumming':
                            category.text = 'gumming'

                    # 如果XML有效，添加文件路径到列表
                    if valid:
                        image_files.append(image_path)
                        xml_files.append(xml_path)
                        # 如果修改了类别，保存更改
                        tree.write(xml_path)

    return image_files, xml_files


# 线程执行的任务
def copy_images_and_xmls(src_folder, image_dst, xml_dst):
    image_files, xml_files = get_image_and_xml_files(src_folder)

    threads = []

    # 为每个图像文件和对应的xml文件创建线程
    for image, xml in zip(image_files, xml_files):
        # 复制图像文件
        thread_image = threading.Thread(target=copy_file, args=(image, image_dst))
        threads.append(thread_image)

        # 复制XML文件
        thread_xml = threading.Thread(target=copy_file, args=(xml, xml_dst))
        threads.append(thread_xml)

    # 启动线程
    for thread in threads:
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()


# 主函数
def main():
    src_folder = 'E:\BaiduNetdiskDownload\Datasets\dataset_init'
    image_dst = 'dataset/VOCdevkit/JPEGImages'
    xml_dst = 'dataset/VOCdevkit/Annotations'

    copy_images_and_xmls(src_folder, image_dst, xml_dst)


if __name__ == "__main__":
    main()
