import numpy as np

__all__ = ["main"]

def bumb_func(x):
    """TODO: Docstring for bumb_func.

    :x: TODO
    :returns: TODO

    """
    return np.exp(1/(4*x*(x-1)))

def smoothing(data_out, smoothness):
    """TODO: Docstring for smoothing.
    :returns: TODO

    """

    x = np.arange(1,smoothness+1)/(smoothness+2)
    f = bumb_func(x)
    f = f/np.sum(f)


    smooth_data_out = data_out.copy()

    n = int(smoothness/2) 
    smooth_data_out[n:-n,0] = np.convolve(data_out[:,0],f, "same")[n:-n]
    smooth_data_out[n:-n,1] = np.convolve(data_out[:,1],f, "same")[n:-n]
    smooth_data_out[n:-n,2] = np.convolve(data_out[:,2],f, "same")[n:-n]

    return smooth_data_out

def main(file_in, file_out, smoothness):
    """TODO: Docstring for main.

    :file_in: TODO
    :file_out: TODO
    :returns: TODO

    """
    data = np.load(file_in)

    
    data_out = []
    for i in range(0,data.shape[0]-1):
        t1, x1, y1, h1 = data[i]
        t2, x2, y2, h2 = data[i+1]


        dt = int(t2-t1)
        df = 1/dt
        for T in range(dt):
            t = T*df
            x = (1-t)*x1 + t*x2 
            y = (1-t)*y1 + t*y2
            h = (1-t)*h1 + t*h2
            data_out.append([int(x+0.5), int(y+0.5), int(h+0.5)])

    data_out.append(data[-1,1:])
    data_out = np.asarray(data_out)
    
    if smoothness>0:
        np.save(file_out, smoothing(data_out,smoothness))

    else:
        np.save(file_out, data_out)


if __name__ == "__main__":
    from sys import argv

    file_in, file_out, smoothness = argv[1:]



    main(file_in, file_out, int(smoothness))
