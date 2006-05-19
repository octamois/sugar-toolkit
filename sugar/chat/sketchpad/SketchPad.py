import pygtk
pygtk.require('2.0')
import gtk
import cairo

from Sketch import Sketch

from SVGdraw import drawing
from SVGdraw import svg

class SketchPad(gtk.DrawingArea):
	def __init__(self):
		gtk.DrawingArea.__init__(self)

		self._active_sketch = None
		self._sketches = []

		self.add_events(gtk.gdk.BUTTON_PRESS_MASK |
						gtk.gdk.BUTTON1_MOTION_MASK)
		self.connect("button-press-event", self.__button_press_cb)
		self.connect("button-release-event", self.__button_release_cb)
		self.connect("motion-notify-event", self.__motion_notify_cb)
		self.connect('expose_event', self.expose)

	def expose(self, widget, event):
		rect = self.get_allocation()
		ctx = widget.window.cairo_create()
		
		for sketch in self._sketches:
			sketch.draw(ctx)
		
		return False

	def add_sketch(self, sketch):
		self._sketches.append(sketch)
	
	def __button_press_cb(self, widget, event):
		self._active_sketch = Sketch()
		self.add_sketch(self._active_sketch)
	
	def __button_release_cb(self, widget, event):
		self._active_sketch = None
	
	def __motion_notify_cb(self, widget, event):
		if self._active_sketch:
			self._active_sketch.add_point(event.x, event.y)
		self.window.invalidate_rect(None, False)
	
	def to_svg(self):
		d = drawing()
		s = svg()
		for sketch in self._sketches:
			s.addElement(sketch.draw_to_svg())
		d.setSVG(s)
		return d.toXml()

def test_quit(w, sketchpad):
	print sketchpad.to_svg()
	gtk.main_quit()

if __name__ == "__main__":
	window = gtk.Window()
	window.set_default_size(400, 300)
	window.connect("destroy", lambda w: gtk.main_quit())
        
	sketchpad = SketchPad()
	window.add(sketchpad)
	sketchpad.show()
	
	window.show()
	
	window.connect("destroy", test_quit, sketchpad)

	gtk.main()
