def enum(**named_values):
	return type('Enum', (), named_values)

Color = enum(RED='red', GREEN='green', BLUE='blue')
Shape = enum(SQUIGGLE='squiggle', DIAMOND='diamond', PILL='pill')
Shading = enum(SOLID='solid',HASHED='hashed',EMPTY='empty')

class Card:
	def __init__(self, number, shading, color, shape):
		self.color = color
		self.shape = shape
		self.number = number
		self.shading = shading

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.color == other.color and self.shape == other.shape and self.number == other.number and self.shading == other.shading
		else:
			return false

	def __ne__(self, other):
		return not self.__eq__(other)

	def __hash__(self):
		return hash((self.number, self.color, self.shading, self.shape))

	def __str__(self):
		plural = False
		if self.number > 1:
			plural = True

		ending = ""
		if plural:
			ending = "s"
		return str(self.number) + " " + self.shading + " " + self.color + " " + self.shape + ending

def isValid(set):
	if len(set) == 1 or len(set) ==3:
		return True

	return False

def isSet(card1, card2, card3):
	colors = set()
	shapes = set()
	shadings = set()
	numbers = set()

	numbers.add(card1.number)
	numbers.add(card2.number)
	numbers.add(card3.number)

	shadings.add(card1.shading)
	shadings.add(card2.shading)
	shadings.add(card3.shading)

	colors.add(card1.color)
	colors.add(card2.color)
	colors.add(card3.color)

	shapes.add(card1.shape)
	shapes.add(card2.shape)
	shapes.add(card3.shape)

	if not isValid(numbers):
		return False

	if not isValid(colors):
		return False

	if not isValid(shadings):
		return False

	if not isValid(shapes):
		return False

	return True

def findSet(cards):
	num_cards = len(cards)
	for i in range(num_cards):
		card1 = cards[i]
		for j in range(i+1, num_cards):
			card2 = cards[j]
			for k in range(j+1, num_cards):
				card3 = cards[k]
				if isSet(card1, card2, card3):
					print "Set: {" + str(card1) + ", " + str(card2) + ", " + str(card3)

cards = list()

cards.append(Card(3, Shading.EMPTY, Color.BLUE, Shape.DIAMOND))
cards.append(Card(2, Shading.EMPTY, Color.GREEN, Shape.DIAMOND))
cards.append(Card(1, Shading.EMPTY, Color.RED, Shape.DIAMOND))

cards.append(Card(3, Shading.SOLID, Color.BLUE, Shape.DIAMOND))
cards.append(Card(3, Shading.SOLID, Color.RED, Shape.SQUIGGLE))
cards.append(Card(1, Shading.HASHED, Color.GREEN, Shape.PILL))

cards.append(Card(2, Shading.SOLID, Color.RED, Shape.DIAMOND))
cards.append(Card(3, Shading.EMPTY, Color.BLUE, Shape.PILL))
cards.append(Card(3, Shading.SOLID, Color.BLUE, Shape.PILL))

cards.append(Card(1, Shading.SOLID, Color.GREEN, Shape.PILL))
cards.append(Card(1, Shading.EMPTY, Color.BLUE, Shape.PILL))
cards.append(Card(2, Shading.HASHED, Color.RED, Shape.DIAMOND))

findSet(cards)
