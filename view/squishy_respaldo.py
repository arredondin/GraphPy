import math
import random
import time
import cairo
from gi.repository import Gtk,Gdk

class Node:

	def __init__(self, id=-1, position=None, label=None):
		self.__id = id
		self.__label = label
		self.__position = position
			
	def set_label(self, newLabel):
		try:
			self.__label = newLabel
			return True
		except:
			return False
	
	def get_label(self):
		try:
			return self.__label
		except:
			return None
	
	def set_id(self, newId):
		try:
			self.__id = newId
			return True
		except:
			return False

	def get_id(self):
		try:
			return self.__id
		except:
			return None
	
	def set_position(self, newPosition):
		try:
			self.__position = newPosition
			return True
		except:
			return False

	def get_position(self):
		try:
			return self.__position
		except:
			return None

	def __str__(self):
		return "NODO ID: {0:d}\n".format(self.__id)


class Edge:
	
	def __init__(self, weight, connection):
		self.__weight = weight
		self.__connection = connection
	
	def set_connection(self, newConnection):
		try:
			self.__connection = newConnection
			return True
		except:
			return False
	
	def get_connection(self):
		try:
			return self.__connection
		except:
			return None
	
	def set_weight(self, newWeight):
		try:
			self.__weight = newWeight
			return True
		except:
			return False
	
	def get_weight(self):
		try:
			return self.__weight
		except:
			return None
	
	def __str__(self):
		return  "ARISTA CONEXION : ({0:d},{1:d})\n ".format(self.__connection[0],self.__connection[1])

class Graph:

	def __init__(self):
		self.__nodes = []
		self.__edges = []
	
	def new_node(self, id, et, pos):
		try:
			tmp = Node(id,pos,et)
			self.__nodes.append(tmp)
			return True
		except:
			return False
	
	def new_edge(self, weight,connection):
		try:
			tmpEdge = Edge(weight,connection)
			self.__edges.append(tmpEdge)
			return True
		except:
			return False
	
	def get_nodes(self):
		return self.__nodes

	def get_edges(self):
		return self.__edges
	
	def del_node(self, idTarget):
		try:
			self.__nodes.remove(idTarget)
			return True
		except:
			return False

	def del_edge(self, edgeTarget):
		try:
			self.__aristas.remove(edgeTarget)
			return True
		except:
			return False
	
	def get_node(self, idTarget):
		try:
			for i in self.__nodes:
				if idTarget == i.get_id():
					return i
		except:
			return None
	
	def exist_edge(self, connection):
		for i in self.__edges:
			if i.get_connection() == connection:
				return True
		return False
	

class Squishy:

	def __init__(self, drawArea):
		self.__graph = Graph()
		self.__drawArea = drawArea
		self.__connect_signals_draw()
		self.__status = 1
		self.__ind = 0
		self.__tmpSelection = None
		self.__frameInicio = (0,0) 
		self.__frameFinal = (0,0)
		self.__deltaI = (0,0)
		self.__deltaF = (0,0)
		self.__band = 0
		self.__temp = []
	
	
	def __connect_signals_draw(self):
		self.__drawArea.connect("draw",self.repaint)
		self.__drawArea.add_events(Gdk.ModifierType.BUTTON1_MASK)
		self.__drawArea.add_events(Gdk.EventMask.BUTTON1_MOTION_MASK)
		self.__drawArea.add_events(Gdk.EventMask.BUTTON_RELEASE_MASK)
		self.__drawArea.connect("button-press-event",self.__on_click)
		self.__drawArea.connect("motion-notify-event",self.__on_motion)
		self.__drawArea.connect("button-release-event",self.__on_click_release)
	
	def __draw(self, pdf = False, png = False, jpg = False):
		if pdf is False and png is False and jpg is False:
			sf=cairo.ImageSurface(cairo.FORMAT_ARGB32,600,500)
		else:
			adress = self.__folder + self.__format
			print adress
			if pdf is True:
				sf = cairo.PDFSurface(adress,600,500)	
		
		cntx = cairo.Context(sf);
		nodes = self.__graph.get_nodes()
		edges = self.__graph.get_edges()
		cntx.set_source_rgb(0,0,0)
		for i in nodes:
			pos = i.get_position()
			cntx.arc(pos[0],pos[1], 10, 0, 2*math.pi)
			cntx.fill()
		print edges
		for i in edges:
			nod1 = self.__graph.get_node(i.get_connection()[0])
			nod2 = self.__graph.get_node(i.get_connection()[1])
			cntx.move_to(nod1.get_position()[0],nod1.get_position()[1])
			cntx.line_to(nod2.get_position()[0],nod2.get_position()[1])
			cntx.stroke()
		return sf
		
		
	def get_graph(self):
		try:
			return self.__graph
		except:
			return None
	
	def get_picture(self, strRuta):
		pass
	
	def set_status(self, newStatus):
		try:
			self.__tmpSelection = None
			self.__status = newStatus
			return True
		except:
			return False
	
	def get_status(self):
		return self.__status
	
	def set_graph( self, newGraph):
		try:
			self.__graph = newGraph
			return True
		except:
			return False

	def __over_nodes(self,x ,y ):
		limit = [(x-15,y+15),(x+15,y+15),(x-15,y-15),(x+15,y-15)]
		for i in self.__graph.get_nodes():
			pos = i.get_position()
			if pos[0] >= limit[0][0] and pos[1] <= limit[0][1]:
				if pos[0] <= limit[1][0] and pos[1] <= limit[1][1]:
					if pos[0] >= limit[2][0] and pos[1] >= limit[2][1]:
						if pos[0] <= limit[3][0] and pos[1] >= limit[3][1]:
								return i
		return False
			
	def __over_select(self):
		temp = []
		for i in self.__graph.get_nodes():
			pos = i.get_position()
			if(pos[0] >= self.__frameInicio[0] and pos[0] <= self.__frameFinal[0]):
				if(pos[1] >= self.__frameInicio[1] and pos[1] <= self.__frameFinal[1]):
					ind=len(temp)
					temp.insert(ind, i)
		return temp

	def __over_edge(self, x, y ):
		#Establecer Limite
		for i in self.__graph.get_edges():
			id_nodos = i.get_connection()
			for j in self.__graph.get_nodes():
				if j.get_id() == id_nodos[0]:
					tmpInicio = j.get_position()
				if j.get_id() == id_nodos[1]:
					tmpFinal = j.get_position()
			pend = ( tmpInicio[1] - tmpFinal[1] )/( tmpInicio[0] - tmpFinal[0])
			print pend
			resultado = (pend*(x - tmpInicio[0]))-(y - tmpInicio[1])
			print resultado
			if resultado <= 5 and resultado >= -5:
				return i
		return False

	def __insert_new_node(self, data=None):
		self.__graph.new_node(random.randint(1,1000),"nuevo",(data.x,data.y))
		self.__drawArea.queue_draw()

	def __inser_edge(self, data=None):
		if self.__tmpSelection == None:
			self.__tmpSelection = self.__over_nodes(data.x, data.y)
		else:
			other = self.__over_nodes(data.x, data.y)
			if other is None:
				self.__tmpSelection = None
			else:
				connected = (self.__tmpSelection.get_id(),other.get_id())
				if not self.__graph.exist_edge(connected):
					self.__graph.new_edge(0,connected)
					self.__drawArea.queue_draw()
			self.__tmpSelection = None

	def __select_area(self, data=None):
		if self.__ind == 0:
			self.__frameInicio = self.__drawArea.get_pointer()
		if self.__ind == 1:
			self.__deltaI = self.__drawArea.get_pointer()

	def __select_area_end(self, data=None):
		self.__frameFinal = self.__drawArea.get_pointer()
		print self.__frameFinal
		self.__ind = 1

	def __reset(self):
		print "reset"
		self.__ind = 0
		self.__tmpSelection = None

	def __move_node(self, data=None):
		self.__tmpSelection = None
		tmp = self.__over_nodes(data.x,data.y)
		tmp.set_position((data.x,data.y))
		self.__drawArea.queue_draw()

	def __on_click(self, widget, data=None):
		if data.button == 1:
			if self.__status == 1:
				self.__graph.new_node(random.randint(1,1000),"nuevo",(data.x,data.y))
				self.__drawArea.queue_draw()
			if self.__status == 3:
				if self.__tmpSelection == None:
					self.__tmpSelection = self.__over_nodes(data.x, data.y)
				else:
					other = self.__over_nodes(data.x, data.y)
					if other is None:
						self.__tmpSelection = None
					else:
						connected = (self.__tmpSelection.get_id(),other.get_id())
						if not self.__graph.exist_edge(connected):
							self.__graph.new_edge(0,connected)
							self.__drawArea.queue_draw()
					self.__tmpSelection = None
			if self.__status == 4:
				if self.__ind == 0:
					self.__frameInicio = self.__drawArea.get_pointer()
				if self.__ind == 1:
					self.__deltaI = self.__drawArea.get_pointer()

		if data.button == 3:
			if self.__status == 4:
				print "reset"
				self.__ind = 0
				self.__tmpSelection = None
		return True

	def __on_click_release(self, widget, data=None):
		if self.__status == 4 and self.__ind == 0 and data.button == 1:
			self.__frameFinal = self.__drawArea.get_pointer()
			print self.__frameFinal
			self.__ind = 1
				
	def __selectMove(self, data=None):
		xInicial, yInicial = self.__deltaI
		x = data.x - xInicial
		y = data.y - yInicial
		for i in self.__temp:
			pos = i.get_position()
			i.set_position((pos[0]+x,pos[1]+y))		
	
	def __on_motion(self, widget, data=None):
		if self.__status == 2:
			self.__tmpSelection = None
			tmp = self.__over_nodes(data.x,data.y)
			tmp.set_position((data.x,data.y))
			self.__drawArea.queue_draw()
		if self.__status == 4:
			if self.__ind == 1:
				if self.__tmpSelection == None:
					self.__temp = self.__over_select()
					self.__tmpSelection = True
				self.__selectMove(data)
				self.__drawArea.queue_draw()
				self.__deltaI = (data.x, data.y)

			
	def _on_double_click(self, widget, data=None):
		pass
    
	def repaint(self, widget, event):
		surf = self.__draw()
		self.canvas = context = widget.get_window().cairo_create()
		context.set_source_surface(surf)
		context.paint()
	
	def create_file(self, direction, format):
		self.__folder = direction
		self.__format = format
		if(format == '.pdf'):
			self.__draw(True, False, False)
		if(format == '.png'):
			self.__draw(False, True, False)
		if(format == '.jpg'):
			self.__draw(False, False, True)

	def menu_contextual(self, data=None, option = False):
		if option == False:
			return self.__over_nodes(data.x, data.y)
		if option == True:
			return self.__over_edge(data.x, data.y)


		

		

	

		

