import UGEN.UGen as Ugen
import tensorflow as tf
import tf.keras as k
import k.layers as layers

class discriminator(k.Model):
  def __init__(self, channels=5, kernel_size=3, name='',**kwargs):
    super(discriminator, self).__init__(name=name, **kwargs)
    self.channels = channels
    self.kernel_size = kernel_size
 
    self.conv3D1 = layers.Conv3D(64, (5), strides=(2), padding='same')
    self.leakyReLu1 = layers.LeakyReLU()
    self.dropout1 = layers.Dropout(0.3)

    self.conv3D2 = layers.Conv3D(128, (5), strides=(2), padding='same')
    self.leakyReLu2 = layers.LeakyReLU()
    self.dropout2 = layers.Dropout(0.3)
    

    self.conv3D3 = layers.Conv3D(128, (5), strides=(2), padding='same')
    self.leakyReLu3 = layers.LeakyReLU()
    self.dropout3 = layers.Dropout(0.3)

    

    self.flatten1 = layers.Flatten()
    self.dense1 = layers.Dense(1,activations.sigmoid)

  def call(self, input):
    x = self.conv3D1(input)
    x = self.leakyReLu1(x)
    x = self.dropout1(x)
    x = self.conv3D2 (x)
    x = self.leakyReLu2(x)
    x = self.dropout2(x)
    x = self.conv3D3(x)
    x = self.leakyReLu3(x)
    x = self.dropout3(x)
    x = self.flatten1(x)
    x = self.dense1(x)
  

    return x
  
def discriminator_loss(real_output, fake_output):
    real_loss = cross_entropy(tf.ones_like(real_output), real_output)
    fake_loss = cross_entropy(tf.zeros_like(fake_output), fake_output)
    total_loss = real_loss + fake_loss
    return total_loss

class GAN(k.Model):
    def __init__(self,discriminator,generator):
      self.discriminator = discriminator
      self.generator = generator 
      self.append = layers.Concatenate(axis=1)


    def call(self,inputs):
      self.discriminator.trainable = False
      x = self.generator(inputs)
      x = self.append([inputs,x])
      return self.discriminator(x)
    
def train(GAN, discriminator,epochs,data,batchsize):
 x,y = data
 z = np.ones(x.shape[1])
 for iter in range(epochs):
   GAN.fit(x,z,epochs=1,batch_size = batchsize,shuffle=True)
   discriminator.fit(y,z,epochs=1,batch_size=batchsize,shuffle=True)
