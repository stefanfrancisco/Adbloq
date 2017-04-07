import os

# Lets change working directory to the pictures folder
#os.chdir("/home/rbruce/caffeV2/adbloq/images/")
os.chdir("/home/rbruce/caffeV2/adbloq/insuranceImages/notInsuranceAds/combined")
# confirm working directory by printing it out
print os.getcwd()

# loop over the files in the working directory and printing them out
# for file in os.listdir('C:'):
 # print file
i = 0
for file in os.listdir('/home/rbruce/caffeV2/adbloq/insuranceImages/notInsuranceAds/combined'):
 file_name, file_extension = os.path.splitext(file)
 i += 1
 new_file_name = 'neg{}.jpg'.format(i)
 os.rename(file, new_file_name)

print file_name, file_extension

#/home/rbruce/caffeV2/adbloq/images