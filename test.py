def main ():
	test(0,0,b'hello');
	test(0,1);

def test(a, b, c = None):
	if (c != None):
		print ("no data")
	else:
		print ("theres data")
	return;

if __name__ == "__main__":
	main();