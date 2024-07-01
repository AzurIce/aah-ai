import onnxruntime
import numpy as np
import PIL.Image

# 加载模型
onnx_model_path = 'resources/models/skill_ready_cls.onnx'
ort_session = onnxruntime.InferenceSession(onnx_model_path)

# 获取模型的输入信息
input_name = ort_session.get_inputs()[0].name
input_shape = ort_session.get_inputs()[0].shape
input_type = ort_session.get_inputs()[0].type

print(f'输入名称: {input_name}')
print(f'输入形状: {input_shape}')
print(f'输入类型: {input_type}')

# 图像处理部分
input_image_path = 'resources/input/skill_ready/ready/ready1.png'
input_image = PIL.Image.open(input_image_path)

# 调整图像大小为模型期望的输入尺寸，这里假设模型期望输入为 (64, 64)
input_image = input_image.resize((64, 64))
input_image = np.array(input_image, dtype=np.float32)

# 打印原始图像形状
print(f'原始图像形状: {input_image.shape}')

# 将通道维度调整为第二个维度 (C, H, W)
input_image = np.transpose(input_image, (2, 0, 1))

# 添加批处理维度 (N, C, H, W)
input_image = np.expand_dims(input_image, axis=0)

# 打印调整后的输入图像形状
print(f'调整后输入图像的形状: {input_image.shape}')

# 预测输出
outputs = ort_session.run(None, {input_name: input_image})

# 打印模型的输出
print(f'模型的输出: {outputs}')

# 处理输出，找到概率最大的类别索引
predicted_class = np.argmax(outputs[0])

# 打印预测结果
print(f'预测类别索引: {predicted_class}')
