
from fixture.test import attr
from decimal import Decimal
import datetime
from fixture import DataSet
from nose.tools import eq_, raises
from fixture.dataset.converter import *
try:
    import json
except ImportError:
    import simplejson as json
from cStringIO import StringIO
        
class FooData(DataSet):
    class bar:
        name = "call me bar"
        is_alive = False
    class foo:
        name = "name's foo"
        is_alive = True
        
class MuchoData(DataSet):
    class mucho:
        d = datetime.date(2008,1,1)
        dt = datetime.datetime(2008,1,1,2,30,59)
        dec = Decimal("1.45667") 
        fl = float(1.45667)

class DummyError(Exception):
    pass
        
class TestDatasetToJson(object):
    
    @attr(unit=1)
    @raises(TypeError)
    def test_must_be_dataset(self):
        class NotADataSet(object):
            pass
        dataset_to_json(NotADataSet)
    
    @attr(unit=1)
    def test_convert_cls(self):
        eq_(dataset_to_json(FooData),
            json.dumps(
            [{'name': "call me bar",
              'is_alive': False},
             {'name': "name's foo",
              'is_alive': True}]))
              
    @attr(unit=1)
    def test_convert_instance(self):
        foo = FooData()
        eq_(dataset_to_json(foo),
            json.dumps(
            [{'name': "call me bar",
              'is_alive': False},
             {'name': "name's foo",
              'is_alive': True}]))
    
    @attr(unit=1)
    def test_dump_to_file(self):
        fp = StringIO()
        dataset_to_json(FooData, fp=fp)
        eq_(fp.getvalue(),
            json.dumps(
            [{'name': "call me bar",
              'is_alive': False},
             {'name': "name's foo",
              'is_alive': True}]))
              
    @attr(unit=1)
    def test_types(self):
        eq_(json.loads(dataset_to_json(MuchoData)),
            [{
                'd': "2008-01-01",
                "dt": "2008-01-01 02:30:59",
                "dec": "1.45667",
                "fl": 1.45667
            }])
    
    @attr(unit=1)
    @raises(DummyError)
    def test_custom_converter(self):
        
        def my_default(obj):
            raise DummyError()
            
        ds = dataset_to_json(MuchoData, default=my_default)
        assert not ds, (
            "dataset_to_json() should have died but it returned: %s" % ds)
            
    @attr(unit=1)
    def test_wrap(self):
        
        def wrap_in_dict(objects):
            return {'data': objects}
            
        eq_(dataset_to_json(FooData, wrap=wrap_in_dict),
            json.dumps({
                'data':
                    [{'name': "call me bar",
                      'is_alive': False},
                     {'name': "name's foo",
                      'is_alive': True}]
                }))
                