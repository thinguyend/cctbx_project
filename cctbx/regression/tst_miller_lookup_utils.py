from __future__ import division, print_function
from builtins import range
from cctbx.array_family import flex
from cctbx import crystal
from cctbx import miller
from cctbx import uctbx
from cctbx import miller


class miller_lookup_utils_tester(object):
  def __init__(self):
    ## define a unit cell
    self.unit_cell = uctbx.unit_cell('20, 30, 40, 90.0, 90.0, 90.0')
    ## space group P1
    self.mi = flex.miller_index( (
      ( -3 , -3 , -3 ),
      ( -3 , -3 , -2 ),
      ( -3 , -3 , -1 ),
      ( -3 , -3 , 0 ),
      ( -3 , -3 , 1 ),
      ( -3 , -3 , 2 ),
      ( -3 , -3 , 3 ),
      ( -3 , -2 , -3 ),
      ( -3 , -2 , -2 ),
      ( -3 , -2 , -1 ),
      ( -3 , -2 , 0 ),
      ( -3 , -2 , 1 ),
      ( -3 , -2 , 2 ),
      ( -3 , -2 , 3 ),
      ( -3 , -1 , -3 ),
      ( -3 , -1 , -2 ),
      ( -3 , -1 , -1 ),
      ( -3 , -1 , 0 ),
      ( -3 , -1 , 1 ),
      ( -3 , -1 , 2 ),
      ( -3 , -1 , 3 ),
      ( -3 , 0 , -3 ),
      ( -3 , 0 , -2 ),
      ( -3 , 0 , -1 ),
      ( -3 , 0 , 0 ),
      ( -3 , 0 , 1 ),
      ( -3 , 0 , 2 ),
      ( -3 , 0 , 3 ),
      ( -3 , 1 , -3 ),
      ( -3 , 1 , -2 ),
      ( -3 , 1 , -1 ),
      ( -3 , 1 , 0 ),
      ( -3 , 1 , 1 ),
      ( -3 , 1 , 2 ),
      ( -3 , 1 , 3 ),
      ( -3 , 2 , -3 ),
      ( -3 , 2 , -2 ),
      ( -3 , 2 , -1 ),
      ( -3 , 2 , 0 ),
      ( -3 , 2 , 1 ),
      ( -3 , 2 , 2 ),
      ( -3 , 2 , 3 ),
      ( -3 , 3 , -3 ),
      ( -3 , 3 , -2 ),
      ( -3 , 3 , -1 ),
      ( -3 , 3 , 0 ),
      ( -3 , 3 , 1 ),
      ( -3 , 3 , 2 ),
      ( -3 , 3 , 3 ),
      ( -2 , -3 , -3 ),
      ( -2 , -3 , -2 ),
      ( -2 , -3 , -1 ),
      ( -2 , -3 , 0 ),
      ( -2 , -3 , 1 ),
      ( -2 , -3 , 2 ),
      ( -2 , -3 , 3 ),
      ( -2 , -2 , -3 ),
      ( -2 , -2 , -2 ),
      ( -2 , -2 , -1 ),
      ( -2 , -2 , 0 ),
      ( -2 , -2 , 1 ),
      ( -2 , -2 , 2 ),
      ( -2 , -2 , 3 ),
      ( -2 , -1 , -3 ),
      ( -2 , -1 , -2 ),
      ( -2 , -1 , -1 ),
      ( -2 , -1 , 0 ),
      ( -2 , -1 , 1 ),
      ( -2 , -1 , 2 ),
      ( -2 , -1 , 3 ),
      ( -2 , 0 , -3 ),
      ( -2 , 0 , -2 ),
      ( -2 , 0 , -1 ),
      ( -2 , 0 , 0 ),
      ( -2 , 0 , 1 ),
      ( -2 , 0 , 2 ),
      ( -2 , 0 , 3 ),
      ( -2 , 1 , -3 ),
      ( -2 , 1 , -2 ),
      ( -2 , 1 , -1 ),
      ( -2 , 1 , 0 ),
      ( -2 , 1 , 1 ),
      ( -2 , 1 , 2 ),
      ( -2 , 1 , 3 ),
      ( -2 , 2 , -3 ),
      ( -2 , 2 , -2 ),
      ( -2 , 2 , -1 ),
      ( -2 , 2 , 0 ),
      ( -2 , 2 , 1 ),
      ( -2 , 2 , 2 ),
      ( -2 , 2 , 3 ),
      ( -2 , 3 , -3 ),
      ( -2 , 3 , -2 ),
      ( -2 , 3 , -1 ),
      ( -2 , 3 , 0 ),
      ( -2 , 3 , 1 ),
      ( -2 , 3 , 2 ),
      ( -2 , 3 , 3 ),
      ( -1 , -3 , -3 ),
      ( -1 , -3 , -2 ),
      ( -1 , -3 , -1 ),
      ( -1 , -3 , 0 ),
      ( -1 , -3 , 1 ),
      ( -1 , -3 , 2 ),
      ( -1 , -3 , 3 ),
      ( -1 , -2 , -3 ),
      ( -1 , -2 , -2 ),
      ( -1 , -2 , -1 ),
      ( -1 , -2 , 0 ),
      ( -1 , -2 , 1 ),
      ( -1 , -2 , 2 ),
      ( -1 , -2 , 3 ),
      ( -1 , -1 , -3 ),
      ( -1 , -1 , -2 ),
      ( -1 , -1 , -1 ),
      ( -1 , -1 , 0 ),
      ( -1 , -1 , 1 ),
      ( -1 , -1 , 2 ),
      ( -1 , -1 , 3 ),
      ( -1 , 0 , -3 ),
      ( -1 , 0 , -2 ),
      ( -1 , 0 , -1 ),
      ( -1 , 0 , 0 ),
      ( -1 , 0 , 1 ),
      ( -1 , 0 , 2 ),
      ( -1 , 0 , 3 ),
      ( -1 , 1 , -3 ),
      ( -1 , 1 , -2 ),
      ( -1 , 1 , -1 ),
      ( -1 , 1 , 0 ),
      ( -1 , 1 , 1 ),
      ( -1 , 1 , 2 ),
      ( -1 , 1 , 3 ),
      ( -1 , 2 , -3 ),
      ( -1 , 2 , -2 ),
      ( -1 , 2 , -1 ),
      ( -1 , 2 , 0 ),
      ( -1 , 2 , 1 ),
      ( -1 , 2 , 2 ),
      ( -1 , 2 , 3 ),
      ( -1 , 3 , -3 ),
      ( -1 , 3 , -2 ),
      ( -1 , 3 , -1 ),
      ( -1 , 3 , 0 ),
      ( -1 , 3 , 1 ),
      ( -1 , 3 , 2 ),
      ( -1 , 3 , 3 ),
      ( 0 , -3 , -3 ),
      ( 0 , -3 , -2 ),
      ( 0 , -3 , -1 ),
      ( 0 , -3 , 0 ),
      ( 0 , -3 , 1 ),
      ( 0 , -3 , 2 ),
      ( 0 , -3 , 3 ),
      ( 0 , -2 , -3 ),
      ( 0 , -2 , -2 ),
      ( 0 , -2 , -1 ),
      ( 0 , -2 , 0 ),
      ( 0 , -2 , 1 ),
      ( 0 , -2 , 2 ),
      ( 0 , -2 , 3 ),
      ( 0 , -1 , -3 ),
      ( 0 , -1 , -2 ),
      ( 0 , -1 , -1 ),
      ( 0 , -1 , 0 ),
      ( 0 , -1 , 1 ),
      ( 0 , -1 , 2 ),
      ( 0 , -1 , 3 ),
      ( 0 , 0 , -3 ),
      ( 0 , 0 , -2 ),
      ( 0 , 0 , -1 ),
      ( 0 , 0 , 0 ),
      ( 0 , 0 , 1 ),
      ( 0 , 0 , 2 ),
      ( 0 , 0 , 3 ),
      ( 0 , 1 , -3 ),
      ( 0 , 1 , -2 ),
      ( 0 , 1 , -1 ),
      ( 0 , 1 , 0 ),
      ( 0 , 1 , 1 ),
      ( 0 , 1 , 2 ),
      ( 0 , 1 , 3 ),
      ( 0 , 2 , -3 ),
      ( 0 , 2 , -2 ),
      ( 0 , 2 , -1 ),
      ( 0 , 2 , 0 ),
      ( 0 , 2 , 1 ),
      ( 0 , 2 , 2 ),
      ( 0 , 2 , 3 ),
      ( 0 , 3 , -3 ),
      ( 0 , 3 , -2 ),
      ( 0 , 3 , -1 ),
      ( 0 , 3 , 0 ),
      ( 0 , 3 , 1 ),
      ( 0 , 3 , 2 ),
      ( 0 , 3 , 3 ),
      ( 1 , -3 , -3 ),
      ( 1 , -3 , -2 ),
      ( 1 , -3 , -1 ),
      ( 1 , -3 , 0 ),
      ( 1 , -3 , 1 ),
      ( 1 , -3 , 2 ),
      ( 1 , -3 , 3 ),
      ( 1 , -2 , -3 ),
      ( 1 , -2 , -2 ),
      ( 1 , -2 , -1 ),
      ( 1 , -2 , 0 ),
      ( 1 , -2 , 1 ),
      ( 1 , -2 , 2 ),
      ( 1 , -2 , 3 ),
      ( 1 , -1 , -3 ),
      ( 1 , -1 , -2 ),
      ( 1 , -1 , -1 ),
      ( 1 , -1 , 0 ),
      ( 1 , -1 , 1 ),
      ( 1 , -1 , 2 ),
      ( 1 , -1 , 3 ),
      ( 1 , 0 , -3 ),
      ( 1 , 0 , -2 ),
      ( 1 , 0 , -1 ),
      ( 1 , 0 , 0 ),
      ( 1 , 0 , 1 ),
      ( 1 , 0 , 2 ),
      ( 1 , 0 , 3 ),
      ( 1 , 1 , -3 ),
      ( 1 , 1 , -2 ),
      ( 1 , 1 , -1 ),
      ( 1 , 1 , 0 ),
      ( 1 , 1 , 1 ),
      ( 1 , 1 , 2 ),
      ( 1 , 1 , 3 ),
      ( 1 , 2 , -3 ),
      ( 1 , 2 , -2 ),
      ( 1 , 2 , -1 ),
      ( 1 , 2 , 0 ),
      ( 1 , 2 , 1 ),
      ( 1 , 2 , 2 ),
      ( 1 , 2 , 3 ),
      ( 1 , 3 , -3 ),
      ( 1 , 3 , -2 ),
      ( 1 , 3 , -1 ),
      ( 1 , 3 , 0 ),
      ( 1 , 3 , 1 ),
      ( 1 , 3 , 2 ),
      ( 1 , 3 , 3 ),
      ( 2 , -3 , -3 ),
      ( 2 , -3 , -2 ),
      ( 2 , -3 , -1 ),
      ( 2 , -3 , 0 ),
      ( 2 , -3 , 1 ),
      ( 2 , -3 , 2 ),
      ( 2 , -3 , 3 ),
      ( 2 , -2 , -3 ),
      ( 2 , -2 , -2 ),
      ( 2 , -2 , -1 ),
      ( 2 , -2 , 0 ),
      ( 2 , -2 , 1 ),
      ( 2 , -2 , 2 ),
      ( 2 , -2 , 3 ),
      ( 2 , -1 , -3 ),
      ( 2 , -1 , -2 ),
      ( 2 , -1 , -1 ),
      ( 2 , -1 , 0 ),
      ( 2 , -1 , 1 ),
      ( 2 , -1 , 2 ),
      ( 2 , -1 , 3 ),
      ( 2 , 0 , -3 ),
      ( 2 , 0 , -2 ),
      ( 2 , 0 , -1 ),
      ( 2 , 0 , 0 ),
      ( 2 , 0 , 1 ),
      ( 2 , 0 , 2 ),
      ( 2 , 0 , 3 ),
      ( 2 , 1 , -3 ),
      ( 2 , 1 , -2 ),
      ( 2 , 1 , -1 ),
      ( 2 , 1 , 0 ),
      ( 2 , 1 , 1 ),
      ( 2 , 1 , 2 ),
      ( 2 , 1 , 3 ),
      ( 2 , 2 , -3 ),
      ( 2 , 2 , -2 ),
      ( 2 , 2 , -1 ),
      ( 2 , 2 , 0 ),
      ( 2 , 2 , 1 ),
      ( 2 , 2 , 2 ),
      ( 2 , 2 , 3 ),
      ( 2 , 3 , -3 ),
      ( 2 , 3 , -2 ),
      ( 2 , 3 , -1 ),
      ( 2 , 3 , 0 ),
      ( 2 , 3 , 1 ),
      ( 2 , 3 , 2 ),
      ( 2 , 3 , 3 ),
      ( 3 , -3 , -3 ),
      ( 3 , -3 , -2 ),
      ( 3 , -3 , -1 ),
      ( 3 , -3 , 0 ),
      ( 3 , -3 , 1 ),
      ( 3 , -3 , 2 ),
      ( 3 , -3 , 3 ),
      ( 3 , -2 , -3 ),
      ( 3 , -2 , -2 ),
      ( 3 , -2 , -1 ),
      ( 3 , -2 , 0 ),
      ( 3 , -2 , 1 ),
      ( 3 , -2 , 2 ),
      ( 3 , -2 , 3 ),
      ( 3 , -1 , -3 ),
      ( 3 , -1 , -2 ),
      ( 3 , -1 , -1 ),
      ( 3 , -1 , 0 ),
      ( 3 , -1 , 1 ),
      ( 3 , -1 , 2 ),
      ( 3 , -1 , 3 ),
      ( 3 , 0 , -3 ),
      ( 3 , 0 , -2 ),
      ( 3 , 0 , -1 ),
      ( 3 , 0 , 0 ),
      ( 3 , 0 , 1 ),
      ( 3 , 0 , 2 ),
      ( 3 , 0 , 3 ),
      ( 3 , 1 , -3 ),
      ( 3 , 1 , -2 ),
      ( 3 , 1 , -1 ),
      ( 3 , 1 , 0 ),
      ( 3 , 1 , 1 ),
      ( 3 , 1 , 2 ),
      ( 3 , 1 , 3 ),
      ( 3 , 2 , -3 ),
      ( 3 , 2 , -2 ),
      ( 3 , 2 , -1 ),
      ( 3 , 2 , 0 ),
      ( 3 , 2 , 1 ),
      ( 3 , 2 , 2 ),
      ( 3 , 2 , 3 ),
      ( 3 , 3 , -3 ),
      ( 3 , 3 , -2 ),
      ( 3 , 3 , -1 ),
      ( 3 , 3 , 0 ),
      ( 3 , 3 , 1 ),
      ( 3 , 3 , 2 ),
      ( 3 , 3 , 3 ) ) )

    ##
    self.xs = crystal.symmetry(self.unit_cell, "P 1")
    self.ms = miller.set(self.xs, self.mi)

    self.tst_all()

  def tst_find_miller(self):
    lookup_function = miller.lookup_tensor(
      self.ms.indices(),
      self.ms.space_group(),True)
    for ii in range(self.ms.indices().size()):
      assert (  ii ==  lookup_function.find_hkl( self.ms.indices()[ii] ) )

  def tst_local_neighbourhood(self):
    local_neighbourhood_size_1_generator = miller.local_neighbourhood(
      self.ms.indices(),
      self.ms.space_group(),
      True,
      1)
    size_1 = local_neighbourhood_size_1_generator.construct_neighbourhood()
    ##-------------
    ## 171 (0, 0, 0)
    ##[122, 164, 170, 172, 178, 220]
    ##---> (-1, 0, 0)
    ##---> (0, -1, 0)
    ##---> (0, 0, -1)
    ##---> (0, 0, 1)
    ##---> (0, 1, 0)
    ##---> (1, 0, 0)
    ##-------------
    ##
    assert (size_1[171].size()==6)
    assert (size_1[171][0]==122)
    assert (size_1[171][1]==164)
    assert (size_1[171][2]==170)
    assert (size_1[171][3]==172)
    assert (size_1[171][4]==178)
    assert (size_1[171][5]==220)

  def tst_local_area(self):
    property = flex.bool(self.ms.indices().size(), True)
    area = miller.local_area(
      self.ms.indices(),
      property,
      self.ms.space_group(),
      True,
      1,
      1,
      1000)
    assert (area.area()[171].size()==7)
    assert (area.area()[171][1]==122)
    assert (area.area()[171][2]==164)
    assert (area.area()[171][3]==170)
    assert (area.area()[171][4]==172)
    assert (area.area()[171][5]==178)
    assert (area.area()[171][6]==220)

    area = miller.local_area(
      self.ms.indices(),
      property,
      self.ms.space_group(),
      True,
      1,
      2,
      1000)
    assert (area.area()[171].size()==25)

    assert (area.area()[171][1]==122)
    assert (area.area()[171][2]==164)
    assert (area.area()[171][3]==170)
    assert (area.area()[171][4]==172)
    assert (area.area()[171][5]==178)
    assert (area.area()[171][6]==220)

    assert (area.area()[171][7]==73)
    assert (area.area()[171][8]==115)
    assert (area.area()[171][9]==121)
    assert (area.area()[171][10]==123)
    assert (area.area()[171][11]==129)
    assert (area.area()[171][12]==157)

    assert (area.area()[171][13]==163)
    assert (area.area()[171][14]==165)
    assert (area.area()[171][15]==213)
    assert (area.area()[171][16]==169)
    assert (area.area()[171][17]==177)
    assert (area.area()[171][18]==219)

    assert (area.area()[171][19]==173)
    assert (area.area()[171][20]==179)
    assert (area.area()[171][21]==221)
    assert (area.area()[171][22]==185)
    assert (area.area()[171][23]==227)
    assert (area.area()[171][24]==269)


  def tst_all(self):
    self.tst_find_miller()
    self.tst_local_neighbourhood()
    self.tst_local_area()
    print("OK")


def run():
  test_miller =  miller_lookup_utils_tester()

run()
