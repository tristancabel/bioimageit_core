import unittest
import os
import os.path
import filecmp

from bioimagepy.data import RawData, ProcessedData
from tests.metadata import create_raw_data, create_processed_data
from bioimagepy.metadata.local import relative_path

class TestLocalData(unittest.TestCase):
    def setUp(self):
        self.ref_rawdata_file = 'tests/test_metadata_local/rawdata.md.json'
        self.tst_rawdata_file = 'tests/test_metadata_local/rawdata_tst.md.json'
        self.ref_processeddata_file = 'tests/test_metadata_local/processeddata.md.json'
        self.tst_processeddata_file = 'tests/test_metadata_local/processeddata_tst.md.json'
        self.ref_processeddata2_file = 'tests/test_metadata_local/processeddata2.md.json'

    def tearDown(self):
        if os.path.isfile(self.tst_rawdata_file): 
            os.remove(self.tst_rawdata_file)
        if os.path.isfile(self.tst_processeddata_file): 
            os.remove(self.tst_processeddata_file) 

    def test_read_rawdata(self):
        raw_data_read = RawData(self.ref_rawdata_file) 
        raw_data_ref_metadata = create_raw_data()
        self.assertEqual(raw_data_read.metadata.serialize(), raw_data_ref_metadata.serialize()) 

    def test_write_rawdata(self):
        raw_data = RawData(self.tst_rawdata_file)
        raw_data.metadata = create_raw_data()
        raw_data.write()
        self.assertTrue(filecmp.cmp(self.tst_rawdata_file, self.ref_rawdata_file, shallow=False))

    def test_read_processeddata(self):
        processed_data_read = ProcessedData(self.ref_processeddata_file)  
        processed_data_ref_metadata = create_processed_data()
        self.assertEqual(processed_data_read.metadata.serialize(), processed_data_ref_metadata.serialize())

    def test_write_processeddata(self):
        processed_data = ProcessedData(self.tst_processeddata_file)
        processed_data.metadata = create_processed_data()
        processed_data.write()
        self.assertTrue(filecmp.cmp(self.tst_processeddata_file, self.ref_processeddata_file, shallow=False))

    def test_processeddata_parent(self):
        processed_data = ProcessedData(self.ref_processeddata2_file)
        parent_data = processed_data.get_parent()
        self.assertEqual(parent_data.metadata.name, 'celegans1_o')

    def test_processeddata_origin(self):
        processed_data = ProcessedData(self.ref_processeddata2_file)
        parent_data = processed_data.get_origin()
        self.assertEqual(parent_data.metadata.name, 'celegans1')