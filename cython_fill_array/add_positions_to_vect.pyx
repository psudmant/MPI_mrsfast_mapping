#import numpy as np
cimport numpy as np
#cimport cython 


#@cython.boundscheck(False)
#@cython.wraparound(False)

#def add_positions_to_vect(np.ndarray[np.uint64_t, ndim=1] depths, np.ndarray[np.uint16_t, ndim=1] gc_content, np.ndarray[np.uint8_t, ndim=1] cp2_unmasked_bool, int max_n_gc):
def add_positions_to_vect(np.ndarray[np.uint16_t, ndim=2] wssd, np.ndarray[np.uint32_t, ndim=1] poses, np.ndarray[np.uint8_t, ndim=1] edits):
    
    cdef Py_ssize_t i
    for i in range(poses.shape[0]):
        wssd[poses[i],edits[i]] +=1
        

