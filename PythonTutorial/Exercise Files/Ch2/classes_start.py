#
# Example file for working with classes
# (For Python 3.x, be sure to use the ExampleSnippets3.txt file)
# self = refers to the object itself, the instance being operated on
# ^ does not have to be called, must be included always

class myClass():
  def method1(self):
    print "myClass method1"
    
  def method2(self, someString):
    print "myClass method2: " + someString

class anotherClass(myClass): #inheriting myClass
  def method2(self):
    print "anotherClass method2"
    
  def method1(self):
    myClass.method1(self);
    print "anotherClass method1"

def main():
  # exercise the class methods
  c = myClass() #instantiates a version of myClass
  c.method1()
  c.method2("This is a string")
  c2 = anotherClass()
  c2.method1()
  c2.method2()

if __name__ == "__main__":
  main()
