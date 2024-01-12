import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from matplotlib.widgets import Slider

def draw(x):
    plt.imshow(x)
    plt.show()

def animate(X, delay = 0.001):
    plt.ion()
    #for step in range(X.shape[2]):
    while True:
        frame = step % X.shape[2]
        plt.imshow(X[:,:,frame], animated=True)
        plt.title('Frame = ' + str(frame))
        plt.pause(delay)
        plt.draw()
        plt.show()
    plt.ioff()

    
# def slider(X):
#     # Create a figure and axis
#     fig, ax = plt.subplots()
#     plt.subplots_adjust(bottom=0.25)
#     ax_slider = plt.axes([0.2, 0.1, 0.65, 0.03])
#     slider = Slider(ax_slider, 'Step', 0, X.shape[2]-1, valinit=0)
#     def update_slider(val):
#         print(X[:,:,int(slider.val)].shape)
#         ax.set_clim(X[:,:,int(slider.val)])
#         fig.canvas.draw()
#         plt.title('Frame = ' + str(int(slider.val)))
#     slider.on_changed(update_slider)

def slider(X):
    # Create a figure and axis
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)
    
    ax_slider = plt.axes([0.2, 0.1, 0.65, 0.03])
    slider = Slider(ax_slider, 'Step', 0, X.shape[2]-1, valinit=0)

    def update_slider(val):
        frame = int(slider.val)
        ax.clear()  # Clear the axis for the new frame
        ax.imshow(X[:, :, frame], cmap='viridis')  # Display the new frame
        ax.set_title('Frame = ' + str(frame))
        fig.canvas.draw()

    slider.on_changed(update_slider)
    
    plt.show()


def E_nearest(X, J=1, periodic_x=False, periodic_y=False):
    E_tmp = 0
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            if i < X.shape[0] - 1 or periodic_x:
                E_tmp += -X[i,j]*X[i+1,j]
            if i > 0 or periodic_x:
                E_tmp += -X[i,j]*X[i-1,j]
            if j < X.shape[1] - 1 or periodic_y:
                E_tmp += -X[i,j]*X[i,j+1]
            if j>0 or periodic_y:
                E_tmp += -X[i,j]*X[i,j-1]
    return J*E_tmp


#k = 1.380649*10**(-23)
#k = 8.617333262*10**(-5)
k=1
T = 2.27
J = 1
#k=1
beta = 1/(k*T)
x_shape = 256
y_shape = 256
periodic_x = False
periodic_y = False
X_initial = 2*np.random.randint(0,2,size=(x_shape,y_shape))-1

number_of_steps = 10000
X_simulation = np.zeros((x_shape, y_shape, number_of_steps+1))
X_simulation[:,:,0] = X_initial


start_time = time.time()
# MH algorithm
number_of_partial_steps = 100
X = X_initial
for step in range(0, number_of_steps):
    print('step ' + str(step) + ' started.')
    for partial_step in range(0, number_of_partial_steps):
        # choose a ranom particle
        i = np.random.randint(0,x_shape)
        j = np.random.randint(0,y_shape)
        dE = 0
        if i < x_shape - 1 or periodic_x:
            dE += X[i,j]*X[i+1,j]
        if i > 0 or periodic_x:
            dE += X[i,j]*X[i-1,j]
        if j < y_shape - 1 or periodic_y:
            dE += X[i,j]*X[i,j+1]
        if j>0 or periodic_y:
            dE += X[i,j]*X[i,j-1]
        dE = 2*J*dE
        if dE < 0:
            X[i,j] = -X[i,j]
        else:
            p = np.random.rand()
            if p < np.exp(-beta*dE):
                X[i,j] = -X[i,j]
            #else:
            #    X_simulation[:,:,step+1] = X_simulation[:,:,step]
    X_simulation[:,:,step+1] = X
end_time = time.time()
print('Excution time = ' + str(end_time - start_time))
#animate(X_simulation, delay=0.01)
slider(X_simulation)


# plt.imshow(X_simulation[:,:,1])
# plt.show()