import json


def convert_predictions(pred_json_path, anno_json_path, output_json_path):
    # Step 1: 加载 COCO 数据集的 annotations 文件
    with open(anno_json_path, 'r') as f:
        coco_data = json.load(f)

    # Step 2: 创建 file_name 和 id 的映射表
    file_name_to_id = {img['file_name']: img['id'] for img in coco_data['images']}

    # Step 3: 加载预测的 predictions.json 文件
    with open(pred_json_path, 'r') as f:
        predictions = json.load(f)

    # Step 4: 修改 prediction.json 中的 image_id 从文件名变为对应的 COCO id
    for pred in predictions:
        # 获取文件名并添加 .jpg 后缀（根据你的 image_id 格式调整）
        file_name = pred['image_id'] + ".jpg"

        # 查找 file_name 对应的 id
        if file_name in file_name_to_id:
            pred['image_id'] = file_name_to_id[file_name]  # 修改为 COCO id
        else:
            print(f"Warning: {file_name} not found in COCO annotations")

    # Step 5: 保存修改后的 prediction.json 文件
    with open(output_json_path, 'w') as f:
        json.dump(predictions, f, indent=4)

    print(f"Conversion complete! Saved to {output_json_path}")

    # parser.add_argument('--anno_json', type=str, default='dataset/val/annotations/val.json',
    #                     help='label coco json path')
    # parser.add_argument('--pred_json', type=str, default='runs/val/exp/predictions.json')
    #

# 调用函数
convert_predictions(
    pred_json_path='runs/val/exp4/predictions.json',
    anno_json_path='dataset/val/annotations/val.json',
    output_json_path='runs/val/exp4/predictions_1.json'
)