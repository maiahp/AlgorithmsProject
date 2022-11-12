import basic_3
import efficient_3
import processfile
import unittest
import plotter

class TestBasicFunctions(unittest.TestCase):
  def test_basic_dp_alg(self):
    self.assertEqual(basic_3.basic_dp_alg("AGT", "AGT")[-1][-1], 0)

  def test_basic_dp_soln(self):
    soln = basic_3.basic_dp_soln("AC", "TATT")
    self.assertEqual(soln[0], 108)
    self.assertEqual(soln[1], "_A_C")
    self.assertEqual(soln[2], "TATT")

  def basic_dp_solution_stc(self, tc):
    data = processfile.main()
    s = data[0][tc]
    outfile_data = data[1][tc]

    soln = basic_3.basic_dp_soln(s[0], s[1])
    # check that the value is correct by comparing it with the data in the outfile
    #print(soln[0], outfile_data[0])
    self.assertEqual(soln[0], outfile_data[0])

    #print(soln[1], soln[2])
    self.assertEqual(soln[1], outfile_data[1])
    self.assertEqual(soln[2], outfile_data[2])

  def test_basic_dp_soln2(self):
    self.basic_dp_solution_stc(0)

  def test_basic_dp_soln3(self):
    self.basic_dp_solution_stc(1)

  def test_basic_dp_soln4(self):
    self.basic_dp_solution_stc(2)

  def test_basic_dp_soln5(self):
    self.basic_dp_solution_stc(3)


class TestEfficientFunctions(unittest.TestCase):

  def test_div_and_conquer(self):
    soln = efficient_3.div_and_conquer("AC", "TATT")
    self.assertEqual(soln[0], 108)
    self.assertEqual(soln[1], "_A_C")
    self.assertEqual(soln[2], "TATT")

  def div_and_conquer_solution_stc(self, tc):
    data = processfile.main()
    s = data[0][tc]
    outfile_data = data[1][tc]

    soln = efficient_3.div_and_conquer(s[0], s[1])
    # check that the value is correct by comparing it with the data in the outfile
    #print(soln[0], outfile_data[0])
    self.assertEqual(soln[0], outfile_data[0])

    #print(soln[1], soln[2])
    self.assertEqual(soln[1], outfile_data[1])
    self.assertEqual(soln[2], outfile_data[2])

  def test_div_and_conquer2(self):
    self.div_and_conquer_solution_stc(0)

  def test_div_and_conquer3(self):
    self.div_and_conquer_solution_stc(1)

  def test_div_and_conquer4(self):
    self.div_and_conquer_solution_stc(2)

  def test_div_and_conquer5(self):
    self.div_and_conquer_solution_stc(3)

class TestProcessFile(unittest.TestCase):

	def test_construct_string(self):
		self.assertEqual(processfile.construct_string("AGTC", [3]), "AGTCAGTC")

plotter.main()
#unittest.main()
#basic.main()
#for e in processfile.main():
#	print(e[0], ":", e[1])