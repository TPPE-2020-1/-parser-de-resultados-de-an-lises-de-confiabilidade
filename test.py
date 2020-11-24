import pytest
from main import (
    read_input_file,
    delimiter_character,
    output_file,
    file_format,
    parse_file_data,
    write_output_file
)

from Exceptions.FormatoSaidaArquivoInvalidoException import FormatoSaidaArquivoInvalidoException
from Exceptions.ArquivoNaoEncontradoException import ArquivoNaoEncontradoException
from Exceptions.DelimitadorInvalidoException import DelimitadorInvalidoException
from Exceptions.EscritaNaoPermitidaException import EscritaNaoPermitidaException
from Exceptions.FormatoArquivoInvalidoException import FormatoArquivoInvalidoException

from mock.file_data_test import file_data_mock1, file_data_mock2
from mock.invalid_file_data import invalid_file_data1, invalid_file_data2
from mock.write_output_test import output_file_mock1, output_file_mock2


# Test Leitura do arquivo de entrada

@pytest.mark.parametrize("input_file,expected", [('./utils/read_file_de.out', 'Datei gelesen'), ('./utils/read_file_en.out', 'File readed'), ('./utils/read_file_fr.out', 'Lecteur de fichiers'), ('./utils/read_file_pt.out', 'Arquivo lido')])
def test_read_input_file(input_file, expected):

    file = read_input_file(input_file)
    assert file == expected


@pytest.mark.parametrize("input_file", [('./utils/read_file_es.out'), ('./test_utils/read_file_en.out')])
def test_read_input_file_not_found(input_file):
    with pytest.raises(ArquivoNaoEncontradoException):
        assert read_input_file(input_file)


# Test Definição do delimitador de campo

@pytest.mark.parametrize("input_file,expected", [(';', ';'), ('\t', '\t'), ('\n', '\n'), ('\r', '\r')])
def test_delimiter_character(input_file, expected):
    assert delimiter_character(input_file) == expected


@pytest.mark.parametrize("input_file", [('Trennzeichen Beispiel'), ('Exemple de délimiteur'), ('Delimiter Example'), ('Exemplo de delimitador')])
def test_invalid_delimiter_character(input_file):
    with pytest.raises(DelimitadorInvalidoException):
        assert delimiter_character(input_file)


# Test Definição do caminho do arquivo de saída.

@pytest.mark.parametrize("directory, file_name, expected", [('utils', 'output_testTab.out', 'utils/output_testTab.out'), ('./', 'other_output_test.out', './other_output_testTab.out')])
def test_output_file(directory, file_name, expected):
    assert output_file(directory, file_name).name == expected


@pytest.mark.parametrize("directory, file_name", [('unexistent_dir/outputs/', 'output_test'), ('../../', 'other_output_test')])
def test_invalid_output_file(directory, file_name):
    with pytest.raises(EscritaNaoPermitidaException):
        assert output_file(directory, file_name)


# Test Definição do formato do arquivo de saída.

@pytest.mark.parametrize("file_format_option, expected", [('colunas', 'colunas'), ('linhas', 'linhas'), ('l', 'l'), ('c', 'c')])
def test_file_format_option(file_format_option, expected):
    assert file_format(file_format_option) == expected


@pytest.mark.parametrize("file_format_option, expected", [('diagonal', 'diagonal'), ('reverso', 'reverso'), ('d', 'd'), ('r', 'r')])
def test_invalid_file_format_option(file_format_option, expected):
    with pytest.raises(FormatoSaidaArquivoInvalidoException):
        assert file_format(file_format_option)


# Test Parser de dados

@pytest.mark.parametrize("file_data, expected", [(file_data_mock1['file_data'], file_data_mock1['parsed_data']), (file_data_mock2['file_data'], file_data_mock2['parsed_data'])])
def test_parse_file_data(file_data, expected):
    parsed_data = parse_file_data(file_data)
    assert parsed_data == expected


@pytest.mark.parametrize("file_data", [(invalid_file_data1), (invalid_file_data2)])
def test_invalid_parse_file_data(file_data):
    with pytest.raises(FormatoArquivoInvalidoException):
        assert parse_file_data(file_data)

# Test Escrita do Arquivo


@pytest.mark.parametrize("parsed_data, delimiter_symbol, output_file, output_format, expected_file",
                         [(output_file_mock1['parsed_data'], output_file_mock1['delimiter_symbol'], output_file_mock1['output_file'],
                           output_file_mock1['output_format'], output_file_mock1['expected_file']),
                          (output_file_mock2['parsed_data'], output_file_mock2['delimiter_symbol'], output_file_mock2['output_file'],
                           output_file_mock2['output_format'], output_file_mock2['expected_file'])])
def test_write_output_file(parsed_data, delimiter_symbol, output_file, output_format, expected_file):
    outputted_file = open(output_file, "w")

    write_output_file(parsed_data, delimiter_symbol,
                      outputted_file, output_format)

    with open(output_file) as res_file:
        with open(expected_file) as exp_file:
            assert res_file.read() == exp_file.read()
