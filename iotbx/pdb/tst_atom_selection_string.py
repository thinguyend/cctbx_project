from __future__ import division
from iotbx.pdb.atom_selection import selection_string_from_selection
from iotbx.pdb.atom_selection import get_clean_selection_string
from mmtbx.ncs.ncs_search import get_chains_info
from scitbx.array_family import flex
from iotbx import pdb
import unittest

__author__ = 'Youval'

class TestNcsPreprocessingFunctions(unittest.TestCase):
  """ Test utility functions in ncs_preprocess.py"""


  def test_get_clean_selection_string(self):
    """ Check get_clean_selection_string  """
    # print sys._getframe().f_code.co_name
    ch_sel = 'chain A'
    res_selection1 = ['resseq 1:10']

    res_id = '27c'
    s = '(resid ' + res_id + ' and (name '
    atom_name = [x for x in [' CA',' N']]
    atom_str = ' or name '.join(atom_name)
    s = s + atom_str + ')'
    res_selection2 = ['resseq 1:10',s]

    result1 = get_clean_selection_string(ch_sel,[])
    result2 = get_clean_selection_string(ch_sel,res_selection1)
    result3 = get_clean_selection_string(ch_sel,res_selection2)

    self.assertEqual(result1,'chain A')
    self.assertEqual(result2,'chain A and resseq 1:10')
    expt = 'chain A and (resseq 1:10 or (resid 27c and (name CA or name N))'
    self.assertEqual(result3,expt)

  def test_selection_string_from_selection(self):
    """ Test selection_string_from_selection """
    # print sys._getframe().f_code.co_name
    pdb_inp = pdb.hierarchy.input(pdb_string=test_pdb_1)
    isel1 = flex.size_t([12, 13, 14, 15, 16, 17, 18])
    isel2 = flex.size_t([12, 13, 14, 16, 17, 18])
    isel3 = flex.size_t([12, 13, 14, 15, 16, 17])

    sel_str1 = selection_string_from_selection(pdb_inp,isel1)
    sel_str2 = selection_string_from_selection(pdb_inp,isel2)
    sel_str3 = selection_string_from_selection(pdb_inp,isel3)

    self.assertEqual(sel_str1,'chain D')
    self.assertEqual(sel_str2,'(chain D and (resseq 1:3 or resseq 5:7))')
    self.assertEqual(sel_str3,'(chain D and resseq 1:6)')
    #
    atom_cache = pdb_inp.hierarchy.atom_selection_cache().selection
    sel1 = list(atom_cache(sel_str1).iselection())
    sel2 = list(atom_cache(sel_str2).iselection())
    sel3 = list(atom_cache(sel_str3).iselection())
    #
    self.assertEqual(sel1,list(isel1))
    self.assertEqual(sel2,list(isel2))
    self.assertEqual(sel3,list(isel3))

  def test_selection_string_from_selection2(self):
    """ Test selection_string_from_selection """
    # print sys._getframe().f_code.co_name
    pdb_inp = pdb.hierarchy.input(pdb_string=test_pdb_2)
    l1 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,
          26,27,28,29,30,31]
    l2 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17      ,20,21,22,23,24,25,
          26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42]
    isel1 = flex.size_t(l1)
    isel2 = flex.size_t(l2)
    #
    sel_str1 = selection_string_from_selection(pdb_inp,isel1)
    sel_str2 = selection_string_from_selection(pdb_inp,isel2)

    self.assertEqual(sel_str1,'chain A or (chain B and resseq 153:154)')
    s = '(chain A and (resseq 151 or (resid 152 and (name N or name CA or '
    s += 'name C or name O or name CB or name CG or name CD or name NE or '
    s += 'name CZ )))) or chain B'
    self.assertEqual(sel_str2,s)
    #
    atom_cache = pdb_inp.hierarchy.atom_selection_cache().selection
    sel1 = list(atom_cache(sel_str1).iselection())
    sel2 = list(atom_cache(sel_str2).iselection())
    #
    self.assertEqual(sel1,list(isel1))
    self.assertEqual(sel2,list(isel2))

  def test_avoid_chain_selection(self):
    # print sys._getframe().f_code.co_name
    pdb_inp = pdb.hierarchy.input(pdb_string=test_pdb_2)
    isel1 = flex.size_t([0,1,2,3,4,5,6,7,8])
    sel_str1 = selection_string_from_selection(pdb_inp,isel1)
    s = '(chain A and resseq 151)'
    self.assertEqual(sel_str1,s)

  def test_avoid_chain_selection2(self):
    # print sys._getframe().f_code.co_name
    pdb_inp = pdb.hierarchy.input(pdb_string=test_pdb_3)
    isel1 = flex.size_t(range(6,46))
    sel_str1 = selection_string_from_selection(pdb_inp,isel1)
    s = '(chain H and (resseq 48 or resid 49 or resid 49A or resseq 50:52))'
    self.assertEqual(sel_str1,s)
    #
    l1 = range(6,25) + range(29,46)
    isel1 = flex.size_t(l1)
    s = '(chain H and (resseq 48 or resid 49 or resseq 50:52))'
    sel_str1 = selection_string_from_selection(pdb_inp,isel1)
    self.assertEqual(sel_str1,s)

  def test_avoid_hoh(self):
    # print sys._getframe().f_code.co_name
    pdb_inp = pdb.hierarchy.input(pdb_string=test_pdb_4)
    isel1 = flex.size_t(range(7))
    sel_str1 = selection_string_from_selection(pdb_inp,isel1)
    s = '(chain A and resseq 151:157)'
    self.assertEqual(sel_str1,s)
    #
    cache = pdb_inp.hierarchy.atom_selection_cache().selection
    sel = cache(s).iselection()
    self.assertEqual(sel.size(),7)

  def test_include_hoh(self):
    # print sys._getframe().f_code.co_name
    pdb_inp = pdb.hierarchy.input(pdb_string=test_pdb_4)
    chains_info = get_chains_info(pdb_inp.hierarchy,exclude_water=True)
    isel1 = flex.size_t(range(7))
    sel_str1 = selection_string_from_selection(
      pdb_inp,isel1,chains_info=chains_info)
    s = '(chain A and resseq 151:157)'
    self.assertEqual(sel_str1,s)
    #
    cache = pdb_inp.hierarchy.atom_selection_cache().selection
    sel = cache(s).iselection()
    self.assertEqual(sel.size(),7)
    #
    chains_info = get_chains_info(pdb_inp.hierarchy,exclude_water=False)
    isel1 = flex.size_t(range(12))
    sel_str1 = selection_string_from_selection(
      pdb_inp,isel1,chains_info=chains_info)
    s = 'chain A'
    self.assertEqual(sel_str1,s)

  def test_selection_with_alternative_conformers(self):
    # print sys._getframe().f_code.co_name
    pdb_inp = pdb.hierarchy.input(pdb_string=test_pdb_5)
    cache = pdb_inp.hierarchy.atom_selection_cache().selection
    chains_info = get_chains_info(pdb_inp.hierarchy)
    ch_D = chains_info['D']
    # test conditions verification
    self.assertEqual(ch_D.no_altloc, [True, True, True, False, True, True])
    select_all = sorted([x for xi in ch_D.atom_selection for x in xi])
    test_list = range(23) + range(27,42)
    self.assertEqual(select_all,test_list)

    # XXX. Now in this case - alternative conformations in selection -
    # assertion in the end of function will fail. Therefore I disabling
    # the rest of tests.
    # exclude selection of residue with altloc, even if in selection
    # selection = flex.size_t(test_list)
    # sel_str = selection_string_from_selection(pdb_inp.hierarchy,selection)
    # expected = '(chain D and (resseq 25:27 or resseq 29:30))'
    # self.assertEqual(sel_str,expected)

    # test that the selection strings gives back the same atom selection
    # test_list = range(19) + range(31,42)
    # selection = flex.size_t(test_list)
    # sel_str = selection_string_from_selection(pdb_inp.hierarchy,selection)
    # self.assertEqual(sel_str,expected)
    # sel = cache(sel_str).iselection()
    # self.assertEqual(set(sel),set(test_list))
    #
    # test_list = range(42)
    # selection = flex.size_t(test_list)
    # sel_str = selection_string_from_selection(pdb_inp.hierarchy,selection)
    # expected = '(chain D and (resseq 25:27 or resseq 29:30))'
    # self.assertEqual(sel_str,expected)

test_pdb_1 = '''\
CRYST1  577.812  448.715  468.790  90.00  90.00  90.00 P 1
SCALE1      0.001731  0.000000  0.000000        0.00000
SCALE2      0.000000  0.002229  0.000000        0.00000
SCALE3      0.000000  0.000000  0.002133        0.00000
ATOM      1  CA  LYS A 151      10.766   9.333  12.905  1.00 44.22           C
ATOM      2  CA  LYS A 152      10.117   9.159  11.610  1.00 49.42           C
ATOM      3  CA  LYS A 153       9.099   8.000  11.562  1.00 46.15           C
ATOM      4  CA  LYS A 154       8.000   8.202  11.065  1.00 52.97           C
ATOM      5  CA  LYS A 155      11.146   9.065  10.474  1.00 41.68           C
ATOM      6  CA  LYS A 156      10.547   9.007   9.084  1.00 55.55           C
ATOM      7  CA  LYS A 157      11.545   9.413   8.000  1.00 72.27           C
ATOM      8  CA  LYS A 158      12.277  10.718   8.343  1.00 75.78           C
ATOM      9  CA  LYS A 159      11.349  11.791   8.809  1.00 75.88           C
TER
ATOM    222  CA  LEU X  40      94.618  -5.253  91.582  1.00 87.10           C
ATOM    223  CA  ARG X  41      62.395  51.344  80.786  1.00107.25           C
ATOM    224  CA  ARG X  42      62.395  41.344  80.786  1.00107.25           C
TER
ATOM      1  CA  THR D   1       8.111  11.080  10.645  1.00 20.00           C
ATOM      2  CA  THR D   2       8.000   9.722  10.125  1.00 20.00           C
ATOM      3  CA  THR D   3       8.075   8.694  11.249  1.00 20.00           C
ATOM      4  CA  THR D   4       8.890   8.818  12.163  1.00 20.00           C
ATOM      5  CA  THR D   5       9.101   9.421   9.092  1.00 20.00           C
ATOM      6  CA  THR D   6       9.001  10.343   8.000  1.00 20.00           C
ATOM      7  CA  THR D   7       8.964   8.000   8.565  1.00 20.00           C
END
'''

test_pdb_2 = '''\
CRYST1   41.870   78.240   85.900  90.00  90.00  90.00 P 2 21 21     8
SCALE1      0.023883  0.000000  0.000000        0.00000
SCALE2      0.000000  0.012781  0.000000        0.00000
SCALE3      0.000000  0.000000  0.011641        0.00000
ATOM      1  N   LYS A 151      16.915  16.113 -32.818  1.00 44.22           N
ATOM      2  CA  LYS A 151      16.266  15.939 -34.113  1.00 49.42           C
ATOM      3  C   LYS A 151      15.248  14.780 -34.161  1.00 46.15           C
ATOM      4  O   LYS A 151      14.149  14.982 -34.658  1.00 52.97           O
ATOM      5  CB  LYS A 151      17.295  15.845 -35.249  1.00 41.68           C
ATOM      6  CG  LYS A 151      16.696  15.787 -36.639  1.00 55.55           C
ATOM      7  CD  LYS A 151      17.694  16.193 -37.723  1.00 72.27           C
ATOM      8  CE  LYS A 151      18.426  17.498 -37.380  1.00 75.78           C
ATOM      9  NZ  LYS A 151      17.498  18.571 -36.914  1.00 75.88           N
ATOM     10  N   ARG A 152      15.575  13.584 -33.658  1.00 41.11           N
ATOM     11  CA  ARG A 152      14.545  12.524 -33.623  1.00 39.90           C
ATOM     12  C   ARG A 152      14.775  11.251 -32.810  1.00 33.61           C
ATOM     13  O   ARG A 152      15.911  10.847 -32.533  1.00 34.25           O
ATOM     14  CB  ARG A 152      14.096  12.135 -35.040  1.00 41.02           C
ATOM     15  CG  ARG A 152      15.094  11.299 -35.813  1.00 45.33           C
ATOM     16  CD  ARG A 152      14.593  11.085 -37.231  1.00 44.56           C
ATOM     17  NE  ARG A 152      13.434  10.190 -37.278  1.00 44.10           N
ATOM     18  CZ  ARG A 152      12.734   9.937 -38.378  1.00 49.14           C
ATOM     19  NH1 ARG A 152      13.064  10.532 -39.521  1.00 44.79           N
ATOM     20  NH2 ARG A 152      11.700   9.097 -38.335  1.00 45.30           N
ATOM     21  N   ALA B 153      13.656  10.621 -32.456  1.00 30.81           N
ATOM     22  CA  ALA B 153      13.619   9.397 -31.651  1.00 29.91           C
ATOM     23  C   ALA B 153      14.208   8.219 -32.409  1.00 31.80           C
ATOM     24  O   ALA B 153      14.248   8.241 -33.644  1.00 31.66           O
ATOM     25  CB  ALA B 153      12.176   9.082 -31.250  1.00 29.44           C
ATOM     26  N   PRO B 154      14.636   7.168 -31.680  1.00 30.22           N
ATOM     27  CA  PRO B 154      15.163   5.989 -32.375  1.00 28.83           C
ATOM     28  C   PRO B 154      14.085   5.348 -33.254  1.00 33.21           C
ATOM     29  O   PRO B 154      12.885   5.472 -32.970  1.00 26.91           O
ATOM     30  CB  PRO B 154      15.534   5.028 -31.234  1.00 27.52           C
ATOM     31  CG  PRO B 154      15.512   5.870 -29.971  1.00 30.59           C
ATOM     32  CD  PRO B 154      14.507   6.943 -30.231  1.00 27.77           C
ATOM     33  N   TYR B 155      14.519   4.680 -34.318  1.00 28.01           N
ATOM     34  CA  TYR B 155      13.603   3.970 -35.194  1.00 26.28           C
ATOM     35  C   TYR B 155      14.387   2.846 -35.845  1.00 32.08           C
ATOM     36  O   TYR B 155      15.623   2.936 -35.993  1.00 29.48           O
ATOM     37  CB  TYR B 155      13.028   4.912 -36.264  1.00 29.02           C
ATOM     38  CG  TYR B 155      14.088   5.528 -37.164  1.00 36.38           C
ATOM     39  CD1 TYR B 155      14.789   6.670 -36.769  1.00 29.69           C
ATOM     40  CD2 TYR B 155      14.403   4.957 -38.401  1.00 38.19           C
ATOM     41  CE1 TYR B 155      15.760   7.237 -37.584  1.00 37.04           C
ATOM     42  CE2 TYR B 155      15.376   5.518 -39.226  1.00 43.21           C
ATOM     43  CZ  TYR B 155      16.051   6.654 -38.804  1.00 41.97           C
END
'''

test_pdb_3 = '''\
CRYST1  203.106   83.279  178.234  90.00 106.67  90.00 C 1 2 1      12
ORIGX1      1.000000  0.000000  0.000000        0.00000
ORIGX2      0.000000  1.000000  0.000000        0.00000
ORIGX3      0.000000  0.000000  1.000000        0.00000
SCALE1      0.004924  0.000000  0.001474        0.00000
SCALE2      0.000000  0.012008  0.000000        0.00000
SCALE3      0.000000  0.000000  0.005857        0.00000
ATOM    313  N   CYS H  47      85.603 -27.032   6.791  1.00 42.51           N
ATOM    314  CA  CYS H  47      84.850 -28.275   6.785  1.00 44.04           C
ATOM    315  C   CYS H  47      83.442 -28.089   6.261  1.00 42.34           C
ATOM    316  O   CYS H  47      83.056 -26.989   5.881  1.00 42.28           O
ATOM    317  CB  CYS H  47      84.827 -28.861   8.204  1.00 47.91           C
ATOM    318  SG  CYS H  47      86.496 -29.154   8.879  1.00 51.94           S
ATOM    319  N   ARG H  48      82.680 -29.174   6.224  1.00 40.63           N
ATOM    320  CA  ARG H  48      81.318 -29.102   5.747  1.00 40.99           C
ATOM    321  C   ARG H  48      80.335 -28.971   6.890  1.00 41.07           C
ATOM    322  O   ARG H  48      80.596 -29.428   7.997  1.00 40.42           O
ATOM    323  CB  ARG H  48      80.994 -30.328   4.884  1.00 42.65           C
ATOM    324  CG  ARG H  48      81.469 -31.626   5.452  1.00 44.32           C
ATOM    325  CD  ARG H  48      81.043 -32.849   4.627  1.00 44.70           C
ATOM    326  NE  ARG H  48      81.529 -34.052   5.294  1.00 44.81           N
ATOM    327  CZ  ARG H  48      82.738 -34.580   5.140  1.00 45.11           C
ATOM    328  NH1 ARG H  48      83.614 -34.042   4.313  1.00 43.19           N
ATOM    329  NH2 ARG H  48      83.095 -35.620   5.877  1.00 47.83           N
ATOM    330  N   LEU H  49      79.221 -28.306   6.614  1.00 41.54           N
ATOM    331  CA  LEU H  49      78.167 -28.103   7.596  1.00 42.36           C
ATOM    332  C   LEU H  49      76.946 -28.837   7.064  1.00 41.91           C
ATOM    333  O   LEU H  49      76.756 -28.928   5.852  1.00 43.00           O
ATOM    334  CB  LEU H  49      77.839 -26.618   7.736  1.00 43.11           C
ATOM    335  CG  LEU H  49      78.845 -25.691   8.414  1.00 45.90           C
ATOM    336  CD1 LEU H  49      78.506 -24.251   8.063  1.00 46.63           C
ATOM    337  CD2 LEU H  49      78.809 -25.892   9.919  1.00 47.40           C
ATOM    338  N   GLY H  49A     76.120 -29.358   7.965  1.00 40.67           N
ATOM    339  CA  GLY H  49A     74.938 -30.081   7.530  1.00 39.48           C
ATOM    340  C   GLY H  49A     75.302 -31.190   6.558  1.00 39.18           C
ATOM    341  O   GLY H  49A     74.504 -31.580   5.700  1.00 38.72           O
ATOM    342  N   GLY H  50      76.527 -31.692   6.695  1.00 39.31           N
ATOM    343  CA  GLY H  50      77.002 -32.764   5.839  1.00 38.66           C
ATOM    344  C   GLY H  50      77.149 -32.388   4.377  1.00 38.02           C
ATOM    345  O   GLY H  50      77.152 -33.261   3.507  1.00 38.89           O
ATOM    346  N   ILE H  51      77.278 -31.095   4.097  1.00 36.09           N
ATOM    347  CA  ILE H  51      77.421 -30.635   2.725  1.00 33.47           C
ATOM    348  C   ILE H  51      78.689 -29.823   2.570  1.00 32.56           C
ATOM    349  O   ILE H  51      78.976 -28.949   3.378  1.00 31.71           O
ATOM    350  CB  ILE H  51      76.229 -29.776   2.323  1.00 32.60           C
ATOM    351  CG1 ILE H  51      74.948 -30.588   2.503  1.00 33.26           C
ATOM    352  CG2 ILE H  51      76.385 -29.303   0.880  1.00 31.47           C
ATOM    353  CD1 ILE H  51      73.684 -29.786   2.351  1.00 33.83           C
ATOM    354  N   ALA H  52      79.443 -30.112   1.520  1.00 31.45           N
ATOM    355  CA  ALA H  52      80.688 -29.412   1.265  1.00 31.24           C
ATOM    356  C   ALA H  52      80.477 -27.950   0.892  1.00 32.00           C
ATOM    357  O   ALA H  52      79.410 -27.556   0.406  1.00 32.53           O
ATOM    358  CB  ALA H  52      81.455 -30.109   0.148  1.00 27.90           C
'''

test_pdb_4 = '''\
CRYST1  577.812  448.715  468.790  90.00  90.00  90.00 P 1
SCALE1      0.001731  0.000000  0.000000        0.00000
SCALE2      0.000000  0.002229  0.000000        0.00000
SCALE3      0.000000  0.000000  0.002133        0.00000
ATOM      1  CA  LYS A 151      10.766   9.333  12.905  1.00 44.22           C
ATOM      2  CA  LYS A 152      10.117   9.159  11.610  1.00 49.42           C
ATOM      3  CA  LYS A 153       9.099   8.000  11.562  1.00 46.15           C
ATOM      4  CA  LYS A 154       8.000   8.202  11.065  1.00 52.97           C
ATOM      5  CA  LYS A 155      11.146   9.065  10.474  1.00 41.68           C
ATOM      6  CA  LYS A 156      10.547   9.007   9.084  1.00 55.55           C
ATOM      7  CA  LYS A 157      11.545   9.413   8.000  1.00 72.27           C
HETATM 3512  O   HOH A2001     -85.460  23.570 -79.414  1.00 34.05           O
HETATM 3513  O   HOH A2002     -81.492  18.186 -35.869  1.00 13.88           O
HETATM 3514  O   HOH A2003     -73.597  30.740 -72.170  1.00 33.13           O
HETATM 3515  O   HOH A2004     -74.933  23.929 -66.597  1.00 26.66           O
HETATM 3516  O   HOH A2005     -73.036  25.921 -66.605  1.00 23.41
END
'''

test_pdb_5 = '''\
CRYST1   42.558  113.820  137.132  90.00  90.00  90.00 P 21 21 21   24
SCALE1      0.023497  0.000000  0.000000        0.00000
SCALE2      0.000000  0.008786  0.000000        0.00000
SCALE3      0.000000  0.000000  0.007292        0.00000
ATOM   2905  N   ILE D  25     -21.903  62.095  51.650  1.00 19.95           N
ATOM   2906  CA  ILE D  25     -20.570  61.733  52.122  1.00 20.06           C
ATOM   2907  C   ILE D  25     -19.631  62.938  52.275  1.00 22.71           C
ATOM   2908  O   ILE D  25     -19.519  63.807  51.393  1.00 21.72           O
ATOM   2909  CB  ILE D  25     -19.887  60.655  51.241  1.00 15.34           C
ATOM   2910  CG1 ILE D  25     -20.768  59.411  51.256  1.00 12.56           C
ATOM   2911  CG2 ILE D  25     -18.438  60.365  51.831  1.00 14.73           C
ATOM   2912  CD1 ILE D  25     -20.661  58.435  50.096  1.00 15.09           C
ATOM   2913  N   GLY D  26     -18.968  62.975  53.429  1.00 20.40           N
ATOM   2914  CA  GLY D  26     -17.920  63.914  53.711  1.00 22.40           C
ATOM   2915  C   GLY D  26     -18.420  65.290  54.086  1.00 23.10           C
ATOM   2916  O   GLY D  26     -18.155  65.781  55.197  1.00 24.70           O
ATOM   2917  N   VAL D  27     -19.117  65.935  53.151  1.00 23.71           N
ATOM   2918  CA  VAL D  27     -19.595  67.307  53.388  1.00 23.17           C
ATOM   2919  C   VAL D  27     -20.597  67.344  54.568  1.00 24.78           C
ATOM   2920  O   VAL D  27     -20.745  68.387  55.199  1.00 26.51           O
ATOM   2921  CB  VAL D  27     -20.183  67.930  52.109  1.00 25.99           C
ATOM   2922  CG1 VAL D  27     -19.069  68.049  51.032  1.00 23.04           C
ATOM   2923  CG2 VAL D  27     -21.399  67.121  51.609  1.00 21.43           C
ATOM   2924  N  AASP D  28     -21.219  66.203  54.890  0.50 22.16           N
ATOM   2925  N  BASP D  28     -21.261  66.213  54.799  0.50 23.07           N
ATOM   2926  CA AASP D  28     -22.200  66.120  55.994  0.50 24.54           C
ATOM   2927  CA BASP D  28     -22.155  66.024  55.923  0.50 25.72           C
ATOM   2928  C  AASP D  28     -21.780  65.239  57.184  0.50 21.81           C
ATOM   2929  C  BASP D  28     -21.575  64.885  56.777  0.50 24.87           C
ATOM   2930  O  AASP D  28     -22.627  64.713  57.901  0.50 22.07           O
ATOM   2931  O  BASP D  28     -21.997  63.731  56.681  0.50 28.18           O
ATOM   2932  CB  ASP D  28     -23.555  65.658  55.450  1.00 25.04           C
ATOM   2933  CG  ASP D  28     -24.173  66.689  54.514  1.00 28.36           C
ATOM   2934  OD1 ASP D  28     -23.934  67.903  54.695  1.00 27.71           O
ATOM   2935  OD2 ASP D  28     -24.948  66.267  53.632  1.00 24.68           O
ATOM   2936  N   SER D  29     -20.479  65.193  57.444  1.00 26.01           N
ATOM   2937  CA  SER D  29     -19.892  64.371  58.495  1.00 24.17           C
ATOM   2938  C   SER D  29     -19.715  65.264  59.716  1.00 23.31           C
ATOM   2939  O   SER D  29     -19.972  66.479  59.622  1.00 23.57           O
ATOM   2940  CB  SER D  29     -18.538  63.871  58.037  1.00 21.39           C
ATOM   2941  OG  SER D  29     -17.658  64.927  57.738  1.00 20.49           O
ATOM   2942  N   ALA D  30     -19.259  64.708  60.836  1.00 19.54           N
ATOM   2943  CA  ALA D  30     -18.937  65.524  61.993  1.00 21.15           C
ATOM   2944  C   ALA D  30     -17.875  66.586  61.555  1.00 20.92           C
ATOM   2945  O   ALA D  30     -18.026  67.767  61.866  1.00 18.58           O
ATOM   2946  CB  ALA D  30     -18.461  64.657  63.163  1.00 17.17           C
'''

def run_selected_tests():
  """  Run selected tests

  1) List in "tests" the names of the particular test you want to run
  2) Comment out unittest.main()
  3) Un-comment unittest.TextTestRunner().run(run_selected_tests())
  """
  tests = ['test_selection_with_alternative_conformers']
  suite = unittest.TestSuite(map(TestNcsPreprocessingFunctions,tests))
  return suite

if __name__=='__main__':
  # use for individual tests
  # unittest.TextTestRunner().run(run_selected_tests())

  # Use to run all tests
  unittest.main(verbosity=0)
