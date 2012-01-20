import os
import sys

from libtbx import easy_pickle
from libtbx.option_parser import option_parser
from scitbx.array_family import flex

from xfel.command_line import view_pixel_histograms # XXX
from xfel.cxi.cspad_ana import cspad_tbx
from xfel.cxi.cspad_ana import xes_finalise

def run(args):
  command_line = (option_parser()
                  .option("--output_dirname", "-o",
                          type="string",
                          help="Directory for output files.")
                  ).process(args=args)
  args = command_line.args
  assert len(args) == 1
  output_dirname = command_line.options.output_dirname
  print output_dirname
  if output_dirname is None:
    output_dirname = os.path.join(os.path.dirname(args[0]), "finalise")
    print output_dirname
  hist_d = easy_pickle.load(args[0])
  pixel_histograms = view_pixel_histograms.pixel_histograms(hist_d)
  xes_from_histograms(pixel_histograms, output_dirname=output_dirname)

def xes_from_histograms(pixel_histograms, output_dirname="."):
  #sum_img = flex.int(flex.grid(391,370), 0) # XXX define the image size some other way?
  sum_img = flex.int(flex.grid(370,391), 0) # XXX define the image size some other way?

  photon_threshold = 20 # XXX
  mask = flex.int(sum_img.accessor(), 0)

  start_row = 370
  end_row = 0

  for i, (pixel, hist) in enumerate(pixel_histograms.histograms.iteritems()):
    start_row = min(start_row, pixel[0])
    end_row = max(end_row, pixel[0])
    n_photons = 0
    gaussians = pixel_histograms.fit_one_histogram(hist)
    zero_peak_diff = gaussians[0].params[1]
    gain = gaussians[1].params[1] - gaussians[0].params[1]
    if abs(gain - 30) > 10:
      print "bad gain!!!!!", pixel
      mask[pixel]
      continue
    i_slot_cutoff = hist.get_i_slot((photon_threshold + zero_peak_diff) * 30/gain)
    #print hist.get_i_slot(photon_threshold), i_slot_cutoff
    slots = hist.slots()
    for i in range(i_slot_cutoff, len(slots)):
      n_photons += slots[i]
    sum_img[pixel] = n_photons

  mask.set_selected(sum_img == 0, 1)
  unbound_pixel_mask = xes_finalise.cspad_unbound_pixel_mask()
  mask.set_selected(unbound_pixel_mask > 0, 1)

  for row in range(sum_img.all()[0]):
    sum_img[row:row+1,:].count(0)

  spectrum_focus = sum_img[start_row:end_row,:]
  mask_focus = mask[start_row:end_row,:]

  d = cspad_tbx.dpack(
    data=spectrum_focus,
    distance=1,
  )
  cspad_tbx.dwritef(d, output_dirname, 'sum_')

  xes_finalise.output_spectrum(spectrum_focus, mask_focus=mask_focus,
                               output_dirname=output_dirname)



if __name__ == '__main__':
  run(sys.argv[1:])
