import dlib
from skimage import io
from scipy.spatial import distance
from Utils import get_image_descriptor
import pandas as pd
from Utils import Profiler



with Profiler() as p:
     d  = get_image_descriptor("test1.jpg")[0]
     print(len(d))
     # exit()

     df = pd.read_csv('dima_and_all.csv')

     desc_list= df.to_records(index=False)

     sort_list= []

with Profiler() as p:
     for row in desc_list:
          desc=list(row)[5:]
          dist= distance.euclidean(d, desc)
          item=[]
          item.append(dist)
          item.append(row[1])
          item.append(row[2])
          sort_list.append(item)
          # print(row[0],row[1],row[2])

     sort_list.sort()
     i2=0
     for i in sort_list:
         print(i)
         if i2==10: break
         i2+=1
     print(len(sort_list))
# print(desc_list[0])

# desc= list(desc_list[0])[5:]

# print(desc)
# if not d: exit()
#
# with open('dima_test.pickle', 'rb') as f:
#     d_list =pickle.load(f)
#

#


# for row in a:
#      row=list(row)
#      dist= distance.euclidean(d, row[5:])
#      row.insert(0,dist)
#      # print(row[0],row[1],row[2])


# a.sort(key= lambda x: x[0])
# #
# for item in a:
#     print(item[0],item[1],item[2])
#
# for i in range(3):
#     # img = io.imread("test/"+str(d_list[i][0])+'.jpg')
#     img = io.imread("test/" + str(d_list[i][0]) + '.jpg')
#     win = dlib.image_window()
#     win.clear_overlay()
#     win.set_image(img)
#     dlib.hit_enter_to_continue()
