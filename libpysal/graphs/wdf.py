from xarray import DataArray
from scipy import sparse
import numpy
from sklearn.preprocessing import LabelEncoder


class W_DF:
    def __init__(self, adjlist):
        self.adjlist = adjlist
        self._cache = dict()

    def neighbors(self, ix):
        # assume that the ix is not iterable, like currently done in W
        return self.adjlist[self.adjlist.focal==ix].neighbor


    def weights(self, ix):
        # assume that the ix is not iterable, like currently done in W
        return self.adjlist[self.adjlist.focal==ix].weight


    @property
    def sparse(self):
        try:
            return self._cache["sparse"]
        except KeyError:
            weights = self.adjlist.weight
            idxs = self.adjlist.focal.unique()
            rows = numpy.searchsorted(idxs, self.adjlist.focal)
            cols = numpy.searchsorted(idxs, self.adjlist.neighbor)
            self._cache["sparse"] = sparse.csr_matrix((weights, (rows, cols)))
            return self.sparse

if __name__ == "__main__":
    import geopandas, libpysal

    counties = geopandas.read_file(libpysal.examples.get_path("NAT.shp"))
    w = libpysal.weights.Rook.from_dataframe(counties, ids=counties.FIPS.tolist())
    alist = w.to_adjlist()
    wd = W_DF(alist)
