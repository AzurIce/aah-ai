import cv2
import onnxruntime as ort
from PIL import Image
import numpy as np

# 置信度
confidence_thres = 0.01
# iou阈值
iou_thres = 0.5
# 类别
classes = {0: 'amiya',
           1: 'kalts',
           2: 'mon3tr',
           3: 'closre',
           4: '12fce',
           5: 'chen',
           6: 'huang',
           7: 'amiya2',
           8: 'lava2',
           9: 'skadi2',
           10: 'chen2',
           11: 'nearl2',
           12: 'agoat2',
           13: 'sora',
           14: 'reed2',
           15: 'kroos2',
           16: 'ghost2',
           17: 'hbisc2',
           18: 'gvial2',
           19: 'greyy2',
           20: 'texas2',
           21: 'yato2',
           22: 'texas',
           23: 'noirc2',
           24: 'slent2',
           25: 'excu2',
           26: 'swire2',
           27: 'jesca2',
           28: 'wisdel',
           29: 'fang2',
           30: 'amiya3',
           31: 'angel',
           32: 'emperor',
           33: 'franka',
           34: 'liskam',
           35: 'silent',
           36: 'fmout',
           37: 'deepcl',
           38: 'siege',
           39: 'cqbw',
           40: 'headbr',
           41: 'myrrh',
           42: 'yuki',
           43: 'hibisc',
           44: 'lava',
           45: 'beagle',
           46: 'fang',
           47: 'kroos',
           48: 'shotst',
           49: 'estell',
           50: 'plosis',
           51: 'bluep',
           52: 'doberm',
           53: 'flameb',
           54: 'mm',
           55: 'ifrit',
           56: 'halo',
           57: 'hsguma',
           58: 'brownb',
           59: 'whitew',
           60: 'nights',
           61: 'ghost',
           62: 'red',
           63: 'prove',
           64: 'shining',
           65: 'nearl',
           66: 'scave',
           67: 'frstar',
           68: 'snakek',
           69: 'myrtle',
           70: 'morgan',
           71: 'tiger',
           72: 'dagda',
           73: 'milu',
           74: 'peacok',
           75: 'hpsts',
           76: 'nightm',
           77: 'skfire',
           78: 'bldsk',
           79: 'svrash',
           80: 'slchan',
           81: 'slbell',
           82: 'cgbird',
           83: 'amgoat',
           84: 'flower',
           85: 'skgoat',
           86: 'frncat',
           87: 'ccheal',
           88: 'helage',
           89: 'clour',
           90: 'falco',
           91: 'frostl',
           92: 'leto',
           93: 'glassb',
           94: 'sunbr',
           95: 'poca',
           96: 'blackd',
           97: 'yak',
           98: 'typhon',
           99: 'cerber',
           100: 'nian',
           101: 'dusk',
           102: 'moeshd',
           103: 'ling',
           104: 'chyue',
           105: 'shu',
           106: 'demkni',
           107: 'platnm',
           108: 'gnosis',
           109: 'melan',
           110: 'ardign',
           111: 'stward',
           112: 'adnach',
           113: 'ansel',
           114: 'mostma',
           115: 'kafka',
           116: 'mantic',
           117: 'cuttle',
           118: 'meteo',
           119: 'grani',
           120: 'bpipe',
           121: 'haak',
           122: 'hmau',
           123: 'savage',
           124: 'jesica',
           125: 'rope',
           126: 'gravel',
           127: 'wyvern',
           128: 'panda',
           129: 'otter',
           130: 'waaifu',
           131: 'cello',
           132: 'mgllan',
           133: 'mlyss',
           134: 'phatom',
           135: 'bibeak',
           136: 'greyy',
           137: 'vodfox',
           138: 'podego',
           139: 'durnar',
           140: 'sddrag',
           141: 'skadi',
           142: 'f12yin',
           143: 'sophia',
           144: 'spikes',
           145: 'strong',
           146: 'astesi',
           147: 'breeze',
           148: 'sqrrel',
           149: 'orchid',
           150: 'excu',
           151: 'popka',
           152: 'catap',
           153: 'midn',
           154: 'spot',
           155: 'medic2',
           156: 'cast3',
           157: 'gyuki',
           158: 'vigna',
           159: 'aglina',
           160: 'thorns',
           161: 'ayer',
           162: 'hamoni',
           163: 'susuro',
           164: 'phenxi',
           165: 'cutter',
           166: 'glaze',
           167: 'zebra',
           168: 'leizi',
           169: 'swire',
           170: 'mudrok',
           171: 'lmlee',
           172: 'bison',
           173: 'glacus',
           174: 'cammou',
           175: 'archet',
           176: 'sidero',
           177: 'folivo',
           178: 'utage',
           179: 'iris',
           180: 'shwaz',
           181: 'sntlla',
           182: 'tknogi',
           183: 'beewax',
           184: 'folnic',
           185: 'aosta',
           186: 'jaksel',
           187: 'ceylon',
           188: 'chiave',
           189: 'surtr',
           190: 'ethan',
           191: 'broca',
           192: 'lisa',
           193: 'saga',
           194: 'toddi',
           195: 'aprl',
           196: 'acdrop',
           197: 'swllow',
           198: 'bena',
           199: 'lionhd',
           200: 'therex',
           201: 'gdglow',
           202: 'asbest',
           203: 'sesa',
           204: 'bubble',
           205: 'snsant',
           206: 'finlpp',
           207: 'mint',
           208: 'rosmon',
           209: 'jnight',
           210: 'pudd',
           211: 'melnte',
           212: 'irene',
           213: 'weedy',
           214: 'lessng',
           215: 'kjera',
           216: 'lunacu',
           217: 'spuria',
           218: 'kazema',
           219: 'puzzle',
           220: 'ncdeer',
           221: 'elysm',
           222: 'rfalcn',
           223: 'aprot2',
           224: 'heyak',
           225: 'tuye',
           226: 'provs',
           227: 'forcer',
           228: 'horn',
           229: 'rockr',
           230: 'chnut',
           231: 'lumen',
           232: 'erato',
           233: 'heidi',
           234: 'ebnhlz',
           235: 'pianst',
           236: 'doroth',
           237: 'malist',
           238: 'bgsnow',
           239: 'absin',
           240: 'totter',
           241: 'quartz',
           242: 'mlynar',
           243: 'judge',
           244: 'highmo',
           245: 'lolxh',
           246: 'peper',
           247: 'ironmn',
           248: 'palico',
           249: 'bdhkgt',
           250: 'haini',
           251: 'lin',
           252: 'warmy',
           253: 'qiubai',
           254: 'chimes',
           255: 'ines',
           256: 'hodrer',
           257: 'ulika',
           258: 'frston',
           259: 'vvana',
           260: 'caper',
           261: 'threye',
           262: 'coldst',
           263: 'almond',
           264: 'bryota',
           265: 'vrdant',
           266: 'baslin',
           267: 'delphn',
           268: 'harold',
           269: 'blkkgt',
           270: 'ray',
           271: 'wanqin',
           272: 'tomimi',
           273: 'zuole',
           274: 'grabds',
           275: 'ela',
           276: 'iana',
           277: 'rdoc',
           278: 'fuze',
           279: 'luton',
           280: 'odda',
           281: 'ascln',
           282: 'logos',
           283: 'cetsyr',
           284: 'phonor',
           285: 'udflow',
           286: 'ulpia',
           287: 'flint',
           288: 'zumama',
           289: 'flamtl',
           290: 'crow',
           291: 'aurora',
           292: 'blemsh',
           293: 'billro',
           294: 'vigil',
           295: 'fartth',
           296: 'ashlok',
           297: 'windft',
           298: 'whispr',
           299: 'mizuki',
           300: 'pinecn',
           301: 'aroma',
           302: 'glider',
           303: 'robin',
           304: 'bstalk',
           305: 'nothin',
           306: 'ash',
           307: 'blitz',
           308: 'rfrost',
           309: 'tachak',
           310: 'cement',
           311: 'qanik',
           312: 'indigo',
           313: 'pasngr',
           314: 'mberry',
           315: 'glady',
           316: 'akafyu',
           317: 'blkngt',
           318: 'kirara',
           319: 'sleach',
           320: 'robrta',
           321: 'pallas',
           322: 'takila',
           323: 'buildr',
           324: 'serum',
           325: 'humus',
           326: 'quercu',
           327: 'firwhl',
           328: 'vendla',
           329: 'wildmn',
           330: 'ctable',
           331: 'inside',
           332: 'kaitou',
           333: 'noirc',
           334: 'durin',
           335: 'nblade',
           336: 'rang',
           337: 'rguard',
           338: 'rcast',
           339: 'rmedic',
           340: 'rsnipe',
           341: 'aguard',
           342: 'acast',
           343: 'amedic',
           344: 'asnipe',
           345: 'aprot',
           346: 'apionr',
           347: 'rdfend'}
# 随机颜色
color_palette = np.random.uniform(100, 255, size=(len(classes), 3))

# 判断是使用GPU或CPU
# providers = [
#     'CUDAExecutionProvider',  # 也可以设置CPU作为备选
# ]
providers = [
    ('CUDAExecutionProvider', {
        'device_id': 0,  # 可以选择GPU设备ID，如果你有多个GPU
    }),
    'CPUExecutionProvider',  # 也可以设置CPU作为备选
]


def calculate_iou(box, other_boxes):
    """
    计算给定边界框与一组其他边界框之间的交并比（IoU）。

    参数：
    - box: 单个边界框，格式为 [x1, y1, width, height]。
    - other_boxes: 其他边界框的数组，每个边界框的格式也为 [x1, y1, width, height]。

    返回值：
    - iou: 一个数组，包含给定边界框与每个其他边界框的IoU值。
    """

    # 计算交集的左上角坐标
    x1 = np.maximum(box[0], np.array(other_boxes)[:, 0])
    y1 = np.maximum(box[1], np.array(other_boxes)[:, 1])
    # 计算交集的右下角坐标
    x2 = np.minimum(box[0] + box[2], np.array(other_boxes)[:, 0] + np.array(other_boxes)[:, 2])
    y2 = np.minimum(box[1] + box[3], np.array(other_boxes)[:, 1] + np.array(other_boxes)[:, 3])
    # 计算交集区域的面积
    intersection_area = np.maximum(0, x2 - x1) * np.maximum(0, y2 - y1)
    # 计算给定边界框的面积
    box_area = box[2] * box[3]
    # 计算其他边界框的面积
    other_boxes_area = np.array(other_boxes)[:, 2] * np.array(other_boxes)[:, 3]
    # 计算IoU值
    iou = intersection_area / (box_area + other_boxes_area - intersection_area)
    return iou


def custom_NMSBoxes(boxes, scores, confidence_threshold, iou_threshold):
    # 如果没有边界框，则直接返回空列表
    if len(boxes) == 0:
        return []
    # 将得分和边界框转换为NumPy数组
    scores = np.array(scores)
    boxes = np.array(boxes)
    # 根据置信度阈值过滤边界框
    mask = scores > confidence_threshold
    filtered_boxes = boxes[mask]
    filtered_scores = scores[mask]
    # 如果过滤后没有边界框，则返回空列表
    if len(filtered_boxes) == 0:
        return []
    # 根据置信度得分对边界框进行排序
    sorted_indices = np.argsort(filtered_scores)[::-1]
    # 初始化一个空列表来存储选择的边界框索引
    indices = []
    # 当还有未处理的边界框时，循环继续
    while len(sorted_indices) > 0:
        # 选择得分最高的边界框索引
        current_index = sorted_indices[0]
        indices.append(current_index)
        # 如果只剩一个边界框，则结束循环
        if len(sorted_indices) == 1:
            break
        # 获取当前边界框和其他边界框
        current_box = filtered_boxes[current_index]
        other_boxes = filtered_boxes[sorted_indices[1:]]
        # 计算当前边界框与其他边界框的IoU
        iou = calculate_iou(current_box, other_boxes)
        # 找到IoU低于阈值的边界框，即与当前边界框不重叠的边界框
        non_overlapping_indices = np.where(iou <= iou_threshold)[0]
        # 更新sorted_indices以仅包含不重叠的边界框
        sorted_indices = sorted_indices[non_overlapping_indices + 1]
    # 返回选择的边界框索引
    return indices


def draw_detections(img, box, score, class_id):
    """
    在输入图像上绘制检测到的对象的边界框和标签。

    参数:
            img: 要在其上绘制检测结果的输入图像。
            box: 检测到的边界框。
            score: 对应的检测得分。
            class_id: 检测到的对象的类别ID。

    返回:
            无
    """

    # 提取边界框的坐标
    x1, y1, w, h = box
    # 根据类别ID检索颜色
    color = color_palette[class_id]
    # 在图像上绘制边界框
    cv2.rectangle(img, (int(x1), int(y1)), (int(x1 + w), int(y1 + h)), color, 2)
    # 创建标签文本，包括类名和得分
    label = f'{classes[class_id]}: {score:.2f}'
    # 计算标签文本的尺寸
    (label_width, label_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    # 计算标签文本的位置
    label_x = x1
    label_y = y1 - 10 if y1 - 10 > label_height else y1 + 10
    # 绘制填充的矩形作为标签文本的背景
    cv2.rectangle(img, (label_x, label_y - label_height), (label_x + label_width, label_y + label_height), color,
                  cv2.FILLED)
    # 在图像上绘制标签文本
    cv2.putText(img, label, (label_x, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)


def preprocess(img, input_width, input_height):
    """
    在执行推理之前预处理输入图像。

    返回:
        image_data: 为推理准备好的预处理后的图像数据。
    """

    # 获取输入图像的高度和宽度
    img_height, img_width = img.shape[:2]
    # 将图像颜色空间从BGR转换为RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # 将图像大小调整为匹配输入形状
    img = cv2.resize(img, (input_width, input_height))
    # 通过除以255.0来归一化图像数据
    image_data = np.array(img) / 255.0
    # 转置图像，使通道维度为第一维
    image_data = np.transpose(image_data, (2, 0, 1))  # 通道首
    # 扩展图像数据的维度以匹配预期的输入形状
    image_data = np.expand_dims(image_data, axis=0).astype(np.float32)
    # 返回预处理后的图像数据
    return image_data, img_height, img_width


def postprocess(input_image, output, input_width, input_height, img_width, img_height):
    """
    对模型输出进行后处理，提取边界框、得分和类别ID。

    参数:
        input_image (numpy.ndarray): 输入图像。
        output (numpy.ndarray): 模型的输出。
        input_width (int): 模型输入宽度。
        input_height (int): 模型输入高度。
        img_width (int): 原始图像宽度。
        img_height (int): 原始图像高度。

    返回:
        numpy.ndarray: 绘制了检测结果的输入图像。
    """

    # 转置和压缩输出以匹配预期的形状
    outputs = np.transpose(np.squeeze(output[0]))
    # 获取输出数组的行数
    rows = outputs.shape[0]
    # 用于存储检测的边界框、得分和类别ID的列表
    boxes = []
    scores = []
    class_ids = []
    # 计算边界框坐标的缩放因子
    x_factor = img_width / input_width
    y_factor = img_height / input_height
    # 遍历输出数组的每一行
    for i in range(rows):
        # 从当前行提取类别得分
        classes_scores = outputs[i][4:]
        # 找到类别得分中的最大得分
        max_score = np.amax(classes_scores)
        # 如果最大得分高于置信度阈值
        if max_score >= confidence_thres:
            # 获取得分最高的类别ID
            class_id = np.argmax(classes_scores)
            # 从当前行提取边界框坐标
            x, y, w, h = outputs[i][0], outputs[i][1], outputs[i][2], outputs[i][3]
            # 计算边界框的缩放坐标
            left = int((x - w / 2) * x_factor)
            top = int((y - h / 2) * y_factor)
            width = int(w * x_factor)
            height = int(h * y_factor)
            # 将类别ID、得分和框坐标添加到各自的列表中
            class_ids.append(class_id)
            scores.append(max_score)
            boxes.append([left, top, width, height])
    # 应用非最大抑制过滤重叠的边界框
    indices = custom_NMSBoxes(boxes, scores, confidence_thres, iou_thres)
    # 遍历非最大抑制后的选定索引
    for i in indices:
        # 根据索引获取框、得分和类别ID
        box = boxes[i]
        score = scores[i]
        class_id = class_ids[i]
        # 在输入图像上绘制检测结果
        draw_detections(input_image, box, score, class_id)
    # 返回修改后的输入图像
    return input_image


def init_detect_model(model_path):
    # 使用ONNX模型文件创建一个推理会话，并指定执行提供者
    session = ort.InferenceSession(model_path, providers=providers)
    # 获取模型的输入信息
    model_inputs = session.get_inputs()
    # 获取输入的形状，用于后续使用
    input_shape = model_inputs[0].shape
    # 从输入形状中提取输入宽度
    input_width = input_shape[2]
    # 从输入形状中提取输入高度
    input_height = input_shape[3]
    # 返回会话、模型输入信息、输入宽度和输入高度
    return session, model_inputs, input_width, input_height


def detect_object(image, session, model_inputs, input_width, input_height):
    # 如果输入的图像是PIL图像对象，将其转换为NumPy数组
    if isinstance(image, Image.Image):
        result_image = np.array(image)
    else:
        # 否则，直接使用输入的图像（假定已经是NumPy数组）
        result_image = image
    # 预处理图像数据，调整图像大小并可能进行归一化等操作
    img_data, img_height, img_width = preprocess(result_image, input_width, input_height)
    # 使用预处理后的图像数据进行推理
    outputs = session.run(None, {model_inputs[0].name: img_data})
    # 对推理结果进行后处理，例如解码检测框，过滤低置信度的检测等
    output_image = postprocess(result_image, outputs, input_width, input_height, img_width, img_height)
    # 返回处理后的图像
    return output_image


if __name__ == '__main__':
    # 模型文件的路径
    model_path = "models/onnx/ready6-6.onnx"
    # 初始化检测模型，加载模型并获取模型输入节点信息和输入图像的宽度、高度
    session, model_inputs, input_width, input_height = init_detect_model(model_path)
    # 三种模式 1为图片预测，并显示结果图片；2为摄像头检测，并实时显示FPS； 3为视频检测，并保存结果视频
    mode = 1
    if mode == 1:
        # 读取图像文件
        image_data = cv2.imread("TestData/readyImages/9.png")
        # 使用检测模型对读入的图像进行对象检测
        result_image = detect_object(image_data, session, model_inputs, input_width, input_height)
        # 将检测后的图像保存到文件
        cv2.imwrite("output_image.png", result_image)
        # 在窗口中显示检测后的图像
        cv2.imshow('Output', result_image)
        # 等待用户按键，然后关闭显示窗口
        cv2.waitKey(0)
    else:
        print("输入错误，请检查mode的赋值")
