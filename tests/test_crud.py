# for unit tests to be available in a subfolder, to avoid package and module errors we must do add the absolute path
# to our root folder, where the files to import are located
import sys
import os
 
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import pytest
from crud import Crud

def test_add_habit():
    crud = Crud()
    
    with pytest.raises(TypeError):
        crud.add_habit("name")