import h5py, numpy
from scipy.io import savemat, loadmat
from basehandler import BaseHandler


class H5_MAT(BaseHandler):
    """Handle Matlab files."""

    def __init__(self, *args, **kwargs):
        super(H5_MAT, self).__init__(*args, **kwargs)


    def read(self):
        matf = loadmat(self.fname,
                squeeze_me=False,
                chars_as_strings=True,
                mat_dtype=True,
                struct_as_record=True)

        for k in ('__header__', '__globals__', '__version__'):
            if matf.has_key(k):
                del matf[k]

        for k in matf.keys():
            if matf[k].dtype == numpy.object: # asume cell of strings
                cell = [unicode(i[0]) for i in matf[k][0]]
                matf[k]=cell

        data = matf
        ordering = matf.keys()

        return {
            'name': self.get_name(),
            'comment': 'matlab',
            'names': [],
            'ordering': ordering,
            'data': data,
        }


    def write(self, data):
        d=data['data']

        for k in d.keys():
            if type(d[k])==list and len(d[k])>0 and type(d[k][0])==str:
                cell = array([ numpy.array(unicode(i)) for i in d[k] ], dtype=numpy.object)
                d[k] = cell
            elif type(d[k])==numpy.ndarray and len(d[k])>0 and d[k][0].dtype == numpy.object:
                cell = numpy.empty((1,len(d[k])), dtype=numpy.object)
                for i in xrange(len(d[k])):
                    cell[0,i]=numpy.array(unicode(d[k][i]), dtype='U')
                d[k] = cell



        savemat(self.fname, d,
                appendmat=False,
                oned_as='row',
                format='5',
                long_field_names=True)
