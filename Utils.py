import os, time
import dlib
from skimage import io
from skimage.color import rgb2gray
import os
import pickle
import pandas as pd


class Profiler(object):
    def __enter__(self):
        self._startTime = time.time()

    def __exit__(self, type, value, traceback):
        print("Elapsed time: {:.3f} sec".format(time.time() - self._startTime))

def extract_descriptors_from_images(load_dir="data"):
    sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
    detector = dlib.get_frontal_face_detector()

    file_list = os.listdir(load_dir)
    faces_count=0
    d_list=[]

    for file_name in file_list:
        path= load_dir+"/"+file_name
        img = io.imread(path)
        dets = detector(img, 1)
        if len(dets)== 0:
            print("В файле {} не найдено лицо".format(file_name))
            continue

        for k, d in enumerate(dets):
            # print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            #     k, d.left(), d.top(), d.right(), d.bottom()))
            shape = sp(img, d)

            print("Обработка файла {}".format(file_name))
            face_descriptor = facerec.compute_face_descriptor(img, shape)
            ar=list(face_descriptor)
            ar.insert(0,file_name.replace('.jpg',''))
            d_list.append(ar)
            faces_count+=1

    print("Получено {} файлов. Найдено {} изображений с лицами".format(len(file_list),faces_count))
    return d_list

def extract_and_save_descriptors_from_images(load_dir="data",p_filename='data.pickle'):

    sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
    detector = dlib.get_frontal_face_detector()

    file_list = os.listdir(load_dir)
    faces_count=0
    d_list=[]

    for file_name in file_list:
        path= load_dir+"/"+file_name
        img = io.imread(path)
        dets = detector(img, 1)
        if len(dets)== 0:
            print("В файле {} не найдено лицо".format(file_name))
            continue

        for k, d in enumerate(dets):
            # print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            #     k, d.left(), d.top(), d.right(), d.bottom()))
            shape = sp(img, d)

            print("Обработка файла {}".format(file_name))
            face_descriptor = facerec.compute_face_descriptor(img, shape)
            ar=list(face_descriptor)
            ar.insert(0,file_name)
            d_list.append(ar)
            faces_count+=1

    print("Получено {} файлов. Найдено {} изображений с лицами".format(len(file_list),faces_count))


    with open(p_filename, 'wb') as f:
         pickle.dump(d_list, f)

# def add_descriptors_from_vk(userid):


def get_image_descriptor(image):

    sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
    detector = dlib.get_frontal_face_detector()

    img= io.imread(image)
    # print(img.shape)
    # img = rgb2gray(img)

    dets = detector(img, 1)
    face_descriptors=[]

    if len(dets)==0:
        print('на фотке не найдено лицо '+image)
        return face_descriptors

    for k, d in enumerate(dets):

        # print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
        #     k, d.left(), d.top(), d.right(), d.bottom()))
        shape = sp(img, d)
    # face_descriptor = list(facerec.compute_face_descriptor(img, shape))
    # face_descriptors.append(face_descriptor)
        try:
            face_descriptor = list(facerec.compute_face_descriptor(img, shape))
            face_descriptors.append(face_descriptor)
        except Exception:
            print('ошибка')



    return face_descriptors

def add_descriptors(sourse_dir,filename='data.pickle', dest_dir=''):
    with open(filename, 'rb') as f:
        d_list = pickle.load(f)


    new_list= extract_descriptors_from_images(sourse_dir)

    if (len(new_list)==0) :
        print("Ни одного лица не найдено")
        return 0

    for item in new_list:
        d_list.append(item)

    with open(filename, 'wb') as f:
        pickle.dump(d_list, f)


def join_desc_files(imput_dir, output_file_name):

    file_list = os.listdir(imput_dir)
    files_count=0
    df_list=[]
    print(len(file_list))

    for file_name in file_list:

        path= imput_dir+"/"+file_name
        print(path)
        df = pd.read_csv(path, index_col=0)
        df_list.append(df)
        files_count+=1
        print('Загружен файл {} {} строки'.format(file_name,df.shape[0]))


    merged_df = pd.concat(df_list)
    merged_df.to_csv(output_file_name, encoding='utf-8')
    print('Объединено {} таблиц и {} строк. Сохранено в файле {}'.format(files_count,merged_df.shape[0],output_file_name))


# def get_descriptors_from_url(url, user_id):
#
#     sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
#     facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
#     detector = dlib.get_frontal_face_detector()
#
#     img = io.imread(url)
#     dets = detector(img, 1)
#     if len(dets) == 0:
#         return False
#
#     for k, d in enumerate(dets):
#         # print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
#         #     k, d.left(), d.top(), d.right(), d.bottom()))
#         shape = sp(img, d)
#
#     print("Обработка юзера {}".format(user_id))
#     face_descriptor = facerec.compute_face_descriptor(img, shape)
#     ar = list(face_descriptor)
#     ar.insert(0, user_id)

# extract_descriptors_from_images(load_dir='data100',p_filename='data100.pickle')