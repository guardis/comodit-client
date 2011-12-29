import setup, definitions, sys

def run_tests(module_names):
    for name in module_names:
        test_module = sys.modules[name]
        try:
            print "="*80
            print "Testing module", name
            test_module.test()
            print "OK"
        except Exception, e:
            print "Error:", e.message

def run_setups(module_names):
    for name in module_names:
        test_module = sys.modules[name]
        try:
            print "="*80
            print "Setuping module", name
            test_module.setup()
            print "OK"
        except Exception, e:
            print "Error:", e.message

def run_tear_downs(module_names):
    for name in module_names:
        test_module = sys.modules[name]
        try:
            print "="*80
            print "Tearing down module", name
            test_module.tear_down()
            print "OK"
        except Exception, e:
            print "Error:", e.message

def test_wrapper(module_names):
    """
    """
    setup.setup()
    definitions.define()

    if len(sys.argv) == 1:
        run_tests(module_names)
    elif len(sys.argv) != 2:
        print "This program takes one or no argument"
    else:
        if sys.argv[1] == "setup":
            run_setups(module_names)
        elif sys.argv[1] == "tear_down":
            run_tear_downs(module_names)
        else:
            print "Unrecognized action."
            print "Accepted actions: setup, tear_down"