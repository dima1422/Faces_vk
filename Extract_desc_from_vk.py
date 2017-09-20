# модуль извлекает дескрипторы из vk и сохраняет их в csv-file
import pandas as pd
import time,vk, os
from Utils import get_image_descriptor
import urllib

# range1,range2= 50025000,50030000
range1,range2= 50030000,50036000
step= 2000

#получаем доступ к апишкам vk
login = '79315783962'
password = 'dima1422'
vk_id = '6160258'
# token='a1ff3d1d50e5cb1fc5e84b5781650d0e4d31cc698f7e817f69aa158b77705bd39c6f36c540cd01d314dff'
session = vk.AuthSession(app_id=vk_id, user_login=login, user_password=password)
vkapi = vk.API(session)


#класс для подсчета времени выполнения
class Profiler(object):
    def __enter__(self):
        self._startTime = time.time()

    def __exit__(self, type, value, traceback):
        print("Elapsed time: {:.3f} sec".format(time.time() - self._startTime))

#получение ссылки на фото максимального разрешения. Получает массив с размерами фоток и ссылками, возвращает ссылку
#на фотку максимального размера
def getMaxPhoto(ph_list):
    w, h = 0, 0
    max_photo_link = ""
    for item in ph_list:
        w_new = item['width']
        h_new = item['height']
        if (w_new > w) and (h_new > h):
            w = w_new
            h = h_new
            max_photo_link = item['src']
    return max_photo_link

#извлекает дескриптор из массива ссылок на фотографии
def get_descriptors_from_vk_user(photos_list, id, dir='test_data'):
    i = 1
    # foto_num=1
    desc_list=[]
    while (i <= len(photos_list)) and (i <= 12):
        max_photo_link = getMaxPhoto(photos_list[-i]['sizes'])
        if max_photo_link == '':
            print("пользователь имеет фотки до 2012 года, пофиксить баг")
            i += 1
            continue
        # try:
        #     resource = urllib.request.urlopen(max_photo_link)
        # except Exception:
        #     print(Exception)
        #     continue
        # new_dir=dir+'/'+str(id)
        # if not os.path.exists(new_dir):
        #     os.makedirs(new_dir)
        # file_name = new_dir+"/" + str(foto_num)+'.jpg'
        # file = open(file_name, 'wb')
        # file.write(resource.read())
        # file.close()

        descriptors = get_image_descriptor(max_photo_link)

        if len(descriptors)>0:
            # foto_num+=1
            f=0
            for descriptor in descriptors:
                f+=1
                descriptor.insert(0, f)
                descriptor.insert(0, "без выгрузки")
                descriptor.insert(0, max_photo_link)
                descriptor.insert(0, id)
                desc_list.append(descriptor)

        i += 1

    return desc_list



#110, 104
#получаем список пользователей для указанного города
# users= vkapi.users.search(city=123,  count= 1000, offset = 200)
#
# if len(users) == 1:
#     print("Никого не найдено!")
#     exit()

# user= vkapi.users.get(user_ids=33)
# try:
#     photos_list = vkapi.photos.get(owner_id=33, album_id='profile', photo_sizes=1)
# except Exception as ex:
#     print(ex)
#
# exit()

#лица, для которых сохранены дескрипторы
faces_count=0
#страницы, для которых были найдены дескрипторы
pages_count=0
#список дескрипторов
descriptors_list=[]

count=0

# with Profiler() as p:
#     for user in users[1:]:
#         count+=1
#         id = user['uid']
#         print("Анализируется {} пользовательc id{}".format(count, id))
#         with Profiler() as p:
#             try:
#                 photos_list = vkapi.photos.get(owner_id=id, album_id='profile', photo_sizes=1)
#             except Exception:
#                 print(Exception)
#                 continue
#             user_desc_list = get_descriptors_from_vk_user(photos_list, id)
#             if  len(user_desc_list)==0:
#                 print("У пользователя id {} лицо на фотографиях не найдено".format(id))
#                 continue
#             print("У пользователя id {} найдено {} лиц".format(id, len(user_desc_list)))
#             for item in user_desc_list:
#                 descriptors_list.append(item)
#                 faces_count += 1
#             pages_count+=1
#
#     print("Найдено пользователей {}, распознано лиц {} c {} страниц".format(count, faces_count, pages_count))

columns = ['id','link','filename','face№']
for i in range(1,129):
    columns.append("parametr№"+str(i))

# range1,range2= 50015000,50020000




last_id=range1

with Profiler() as p:
    for id in range(range1,range2):
        count+=1

        print("Анализируется {} пользовательc id{}".format(count, id))

        try:
            photos_list = vkapi.photos.get(owner_id=id, album_id='profile', photo_sizes=1)
        except Exception:
            print(Exception)
            if (id % step == 0 or id == range2 - 1) and id != range1:
                print('трям')
                df = pd.DataFrame.from_records(descriptors_list, columns=columns)
                df.to_csv('without_photo' + str(last_id) + '_' + str(id) + '.csv', encoding='utf-8')
                last_id = id + 1
                descriptors_list = []
            continue

        user_desc_list = get_descriptors_from_vk_user(photos_list, id)

        if  len(user_desc_list)==0:
            print("У пользователя id {} лицо на фотографиях не найдено".format(id))
        else:
            print("У пользователя id {} найдено {} лиц".format(id, len(user_desc_list)))
            for item in user_desc_list:
                descriptors_list.append(item)
                faces_count += 1
            pages_count+=1

        if (id%step == 0 or id ==range2-1) and id != range1:
            print('трям')
            df = pd.DataFrame.from_records(descriptors_list, columns=columns)
            df.to_csv('without_photo' + str(last_id) + '_' + str(id) + '.csv', encoding='utf-8')
            last_id=id+1
            descriptors_list=[]


    print("Найдено пользователей {}, распознано лиц {} c {} страниц".format(count, faces_count, pages_count))




# df = pd.DataFrame.from_records(descriptors_list, columns=columns)
# df.to_csv('without_photo'+str(range1)+'_'+str(range2)+'.csv', encoding='utf-8')
# #
