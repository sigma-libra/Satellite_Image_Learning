from model import *
from data import *

#os.environ["CUDA_VISIBLE_DEVICES"] = "0"


data_gen_args = dict(rotation_range=0.2,
                    width_shift_range=0.05,
                    height_shift_range=0.05,
                    shear_range=0.05,
                    zoom_range=0.05,
                    horizontal_flip=True,
                    fill_mode='nearest')
myGene = trainGenerator(2,'data/roadsegmentation/train','image','label',data_gen_args,save_to_dir = None)

model = unet()
model_checkpoint = ModelCheckpoint('unet_membrane.hdf5', monitor='loss',verbose=1, save_best_only=True)
model.fit_generator(myGene,steps_per_epoch=300,epochs=1,callbacks=[model_checkpoint])

testGene = testGenerator("data/roadsegmentation/test", 50, (608,608))
model = unet(pretrained_weights="unet_membrance.hdf5", input_size = (608,608,1))
#model.load_weights("unet_roads.hdf5")
results = model.predict_generator(testGene,50,verbose=1)
saveResult("data/roadsegmentation/test/predictions",results)