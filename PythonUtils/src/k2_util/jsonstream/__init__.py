import os, json, re
from enum import Enum
from k2_util import numUtil

RE_IS_FLOAT = re.compile('[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?')

class Expects(Enum):
    NAME = 'name'
    VALUE = 'value'
    END_OBJECT = 'end_object'
    END_LIST = 'end_list'
    
class JsonWriterException(Exception):
    pass

class JsonReaderException(Exception):
    pass

def encode(s):
    return json.dumps(s)
        
def decode(s):
    return json.loads(s)

class JsonStates(Enum):
    OPEN = 0
    IN_OBJECT = 1
    IN_OBJECT_WITH_NAME = 2
    IN_OBJECT_WITH_NAME_AND_VALUE = 3
    IN_LIST = 4
    IN_LIST_WITH_VALUE = 5
    CLOSED = 6

class JsonState(object):
    def __init__(self, previous, state):
        self.previous = previous
        self._state = state
        
    def state(self, *args):
        if len(args) > 0:
            self._state = args[0]
        return self._state

class JsonWriter(object):
           
    def __init__(self, writer, **kw):
        self.writer = writer
        self.indent = kw.get('indent', '')
        self.depth = 0
        self.linesep = os.linesep if len(self.indent) > 0 else ''
        self.current_indent = ''
        self.quote = kw.get('quote', JsonToken.QUOTE.value)
        self.varsep = kw.get('varsep', JsonToken.VALUE_SEPARATOR.value)
        self.namesep = kw.get('namesep', JsonToken.NAME_SEPARATOR.value)
        self.startobj = kw.get('start_obj', JsonToken.START_OBJECT.value)
        self.endobj = kw.get('end_obj', JsonToken.END_OBJECT.value)
        self.startlist = kw.get('start_list', JsonToken.START_LIST.value)
        self.endlist = kw.get('end_list', JsonToken.END_LIST.value)
        self.state = JsonState(None, JsonStates.OPEN)
        self.expects = None
        
    def _token(self, token):
        if token == JsonToken.QUOTE: return self.quote
        if token == JsonToken.VALUE_SEPARATOR: return self.varsep
        if token == JsonToken.NAME_SEPARATOR: return self.namesep
        if token == JsonToken.START_OBJECT: return self.startobj
        if token == JsonToken.END_OBJECT: return self.endobj
        if token == JsonToken.START_LIST: return self.startlist
        if token == JsonToken.END_LIST: return self.endlist
        raise ValueError('Expected token as JsonToken')
        
    def _indent(self, state):
        self.debug('_indent("%s")' % state)
        self.depth += 1
        self.current_indent += self.indent
        if self.state.state() == JsonStates.IN_OBJECT or self.state.state() == JsonStates.IN_OBJECT_WITH_NAME:
            self.state.state(JsonStates.IN_OBJECT_WITH_NAME_AND_VALUE)
        elif self.state.state() == JsonStates.IN_LIST:
            self.state.state(JsonStates.IN_LIST_WITH_VALUE)
        self.state = JsonState(self.state, state)
        
    def _outdent(self):
        self.debug('_outdent()')
        if self.depth == 0:
            return
        self.depth -= 1
        self.current_indent = self.current_indent[:-len(self.indent)]
        self.state = self.state.previous
        
    def _check_expects(self, expects):
        if self.expects == None:
            print('Expects anything')
            return
        for ex in self.expects:
            print('Checking expects %s      State: %s      PreviousState: %s' % (ex.value, self.state.state(), self.state.previous.state() if self.state.previous != None else 'None'))
            if ex == expects:
                return
        expected = ''
        for ex in self.expects:
            expected += ex.value+' or '
        expected = expected[:-4]
        raise JsonWriterException('JsonWriter expected a %s but got a %s' % (expected, expects.value))
        
    def _set_expects(self, *expects):
        self.expects = expects
        e = ''
        for ex in self.expects:
            e += ex.value+' '
        print('Expects: %s      State: %s      PreviousState: %s' % (e, self.state.state(), self.state.previous.state() if self.state.previous != None else 'None'))
        
    def debug(self, caller):
        return
        print('%s      State: %s      PreviousState: %s' % (caller, self.state.state(), self.state.previous.state() if self.state.previous != None else 'None'))
        
    def name(self, name):
        self.debug('name("%s")' % name)
#        self._check_expects(Expects.NAME)
        if self.state.state() == JsonStates.IN_OBJECT_WITH_NAME_AND_VALUE:
            self.writer.write(self._token(JsonToken.VALUE_SEPARATOR)+' '+self.linesep)
        self.writer.write(self.current_indent+self._token(JsonToken.QUOTE)+name+self._token(JsonToken.QUOTE)+self._token(JsonToken.NAME_SEPARATOR)+' ')
        if self.state.state() == JsonStates.IN_OBJECT or self.state.state() == JsonStates.IN_OBJECT_WITH_NAME_AND_VALUE:
            self.state.state(JsonStates.IN_OBJECT_WITH_NAME)
#        self._set_expects(Expects.VALUE)
        
    def value(self, value):
        self.debug('value(%s)' % encode(value))
#        self._check_expects(Expects.VALUE)       
        if self.state.state() == JsonStates.IN_LIST_WITH_VALUE:
            self.writer.write(self._token(JsonToken.VALUE_SEPARATOR)+' '+self.linesep)
            
        if self.state.state() == JsonStates.IN_LIST_WITH_VALUE or self.state.state() == JsonStates.IN_LIST:
            self.writer.write(self.current_indent)
        if value == None:
            self.writer.write(encode(value))
        elif isinstance(value, (int, float, str, bool)):
            self.writer.write(encode(value))
        else:
            raise JsonWriterException('JsonWriter only accepts int, float, string, boolean or None as a value')
        
        if self.state.state() == JsonStates.IN_OBJECT_WITH_NAME:
            self.state.state(JsonStates.IN_OBJECT_WITH_NAME_AND_VALUE)
#            self._set_expects(Expects.END_OBJECT, Expects.NAME)
        elif self.state.state() == JsonStates.IN_LIST or self.state.state() == JsonStates.IN_LIST_WITH_VALUE:
            self.state.state(JsonStates.IN_LIST_WITH_VALUE)
#            self._set_expects(Expects.END_LIST, Expects.VALUE)
                   
        
    def begin_object(self):
        self.debug('begin_object()')
        if self.state.state() == JsonStates.IN_OBJECT_WITH_NAME_AND_VALUE or self.state.state() == JsonStates.IN_LIST_WITH_VALUE:
            self.writer.write(self._token(JsonToken.VALUE_SEPARATOR)+' '+self.linesep)
#        self._check_expects(Expects.VALUE)
        if self.state.state() == JsonStates.IN_OBJECT_WITH_NAME_AND_VALUE or self.state.state() == JsonStates.IN_OBJECT_WITH_NAME:
            self.writer.write(self._token(JsonToken.START_OBJECT) + self.linesep)
        else:
            self.writer.write(self.current_indent + self._token(JsonToken.START_OBJECT) + self.linesep)
        self._indent(JsonStates.IN_OBJECT)
#        self._set_expects(Expects.NAME, Expects.END_OBJECT)

    def end_object(self):
        self.debug('end_object()')
        if self.state.state() == JsonStates.IN_OBJECT_WITH_NAME_AND_VALUE or self.state.state() == JsonStates.IN_LIST_WITH_VALUE:
            self.writer.write(self.linesep)
        self._outdent()
        self.writer.write(self.current_indent + self._token(JsonToken.END_OBJECT))

    def begin_list(self):
        self.debug('begin_list()')
        if self.state.state() == JsonStates.IN_OBJECT_WITH_NAME_AND_VALUE or self.state.state() == JsonStates.IN_LIST_WITH_VALUE:
            self.writer.write(self._token(JsonToken.VALUE_SEPARATOR)+' '+self.linesep)
#        self._check_expects(Expects.VALUE)
        if self.state.state() == JsonStates.IN_OBJECT_WITH_NAME:
            self.writer.write(self._token(JsonToken.START_LIST) + self.linesep)
        else:
            self.writer.write(self.current_indent + self._token(JsonToken.START_LIST) + self.linesep)
        self._indent(JsonStates.IN_LIST)
#        self._set_expects(Expects.VALUE, Expects.END_LIST)

    def end_list(self):
        self.debug('end_list()')
        if self.state.state() == JsonStates.IN_OBJECT_WITH_NAME_AND_VALUE or self.state.state() == JsonStates.IN_LIST_WITH_VALUE:
            self.writer.write(self.linesep)
        self._outdent()
        self.writer.write(self.current_indent + self._token(JsonToken.END_LIST))

class JsonToken(Enum):
    START_LIST = '['
    END_LIST = ']'
    START_OBJECT = '{'
    END_OBJECT = '}'
    QUOTE = '"'
    VALUE_SEPARATOR = ','
    NAME_SEPARATOR = ':'
    
class JsonNodeType(Enum):
    START_LIST = 'start_list'
    END_LIST = 'end_list'
    START_OBJECT = 'start_object'
    END_OBJECT = 'end_object'
    NAME = 'name'
    BOOL_VALUE = 'bool_value'
    NUM_VALUE = 'num_value'
    STR_VALUE = 'str_value'
    NULL_VALUE = 'null_value'
    
class JsonNode(object):
    def __init__(self, reader, type):
        self.reader = reader
        self.type = type
        
    def type_is(self, type):
        return self.type == type
        
class JsonStartObjectNode(JsonNode):
    def __init__(self, reader):
        JsonNode.__init__(self, reader, JsonNodeType.START_OBJECT)
        
class JsonEndObjectNode(JsonNode):
    def __init__(self, reader):
        JsonNode.__init__(self, reader, JsonNodeType.END_OBJECT)
        
class JsonStartListNode(JsonNode):
    def __init__(self, reader):
        JsonNode.__init__(self, reader, JsonNodeType.START_LIST)
        
class JsonEndListNode(JsonNode):
    def __init__(self, reader):
        JsonNode.__init__(self, reader, JsonNodeType.END_LIST)
        
class JsonNameNode(JsonNode):
    def __init__(self, reader, name):
        JsonNode.__init__(self, reader, JsonNodeType.NAME)
        self.name = name
 
class JsonValueNode(JsonNode):
    def __init__(self, reader, type):
        JsonNode.__init__(self, reader, type)
    @staticmethod
    def value_node(reader, value):
        if value == None or len(value) == 0 or value.upper() == 'NULL': 
            return JsonNullNode(reader)
        if value.upper() in ['TRUE', 'FALSE']:
            return JsonBooleanNode(reader, value)
        if len(value) >= 2 and value[0] == reader._token(JsonToken.QUOTE) and value[-1:] == reader._token(JsonToken.QUOTE):
            return JsonStringNode(reader, value[1:-1])
        if RE_IS_FLOAT.search(value):
            return JsonNumberNode(reader, value)
        raise JsonReaderException('Invalid value: %s in JSON' % value)
        
        
class JsonBooleanNode(JsonValueNode):
    def __init__(self, reader, value):
        JsonValueNode.__init__(self, reader, JsonNodeType.BOOL_VALUE)
        self.value = value.upper() == 'TRUE'
        
class JsonNumberNode(JsonValueNode):
    def __init__(self, reader, value):
        JsonValueNode.__init__(self, reader, JsonNodeType.NUM_VALUE)
        if '.' in value:
            self.value = float(value)
        else:
            self.value = int(value)
        
class JsonStringNode(JsonValueNode):
    def __init__(self, reader, value):
        JsonValueNode.__init__(self, reader, JsonNodeType.STR_VALUE)
        
class JsonNullNode(JsonValueNode):
    def __init__(self, reader):
        JsonValueNode.__init__(self, reader, JsonNodeType.NULL_VALUE)
    
class JsonReader(object):
    def __init__(self, reader, **kw):
        self.reader = reader
        self.tokeniser = JsonTokeniser(reader)
        self._next = self.tokeniser.get_next_token()

        
    def _move_to_start(self):
        c = self.reader.read(chars=1)
        while c.isspace():
            c = self.reader.read(chars=1)
            
        if c == self._token(JsonToken.START_OBJECT):
            self.next = JsonStartObjectNode(self)
        elif c == self._token(JsonToken.START_LIST):
            self.next = JsonStartListNode(self)
        else:
            raise JsonReaderException('Json documents must start with an object or list')
            
        
        
    def has_next(self):
        return self._next != None
    
    def peek(self):
        return self._next
    
    def next(self):
        self._next = self.tokeniser.get_next_token()
        return self._next
    
    def _check_and_next(self, node_type):
        if not self._next.node_type == node_type:
            raise JsonReaderException('Expected %s but got %s' % (node_type, self._next.node_type))
        next = self._next
        self.next()
        return next

    
    def begin_object(self):
        return self._check_and_next(JsonNodeType.START_OBJECT)
        
    def next_name(self):
        return self._check_and_next(JsonNodeType.NAME)
        
    def next_number(self):
        return self._check_and_next(JsonNodeType.NUM_VALUE)
        
    def next_boolean(self):
        return self._check_and_next(JsonNodeType.BOOL_VALUE)
        
    def next_string(self):
        return self._check_and_next(JsonNodeType.STR_VALUE)
        
    def next_null(self):
        return self._check_and_next(JsonNodeType.NULL_VALUE)
        
    def end_object(self):
        return self._check_and_next(JsonNodeType.END_OBJECT)
        
    def start_list(self):
        return self._check_and_next(JsonNodeType.START_LIST)
        
    def end_list(self):
        return self._check_and_next(JsonNodeType.END_LIST)
        
        
class JsonTokeniserState(Enum):
    STARTING = 0
    EXPECTING_VALUE = 1
    
class Token(object):
    def __init__(self, node_type, **kw):
        self.node_type = node_type
        self.value = kw.get('value', None)

class JsonTokeniser(object):    
    
    def __init__(self, reader, **kw):
        self.path = ''
        self.pos = 0
        self.row = 0
        self.col = 0
        self.reader = reader
        self.quote = kw.get('quote', JsonToken.QUOTE.value)
        self.start_obj = kw.get('start_obj', JsonToken.START_OBJECT.value)
        self.end_obj = kw.get('end_obj', JsonToken.END_OBJECT.value)
        self.start_list = kw.get('start_list', JsonToken.START_LIST.value)
        self.end_list = kw.get('end_list', JsonToken.END_LIST.value)
        self.namesep = kw.get('namesep', JsonToken.NAME_SEPARATOR.value)
        self.valuesep = kw.get('valuesep', JsonToken.VALUE_SEPARATOR.value)
        self.debugging = kw.get('debug', False)
        self.escape = '\\'
        self.token_value = ''
        self.token_value_quoted = False
        self.escaping = False
        self.in_quotes = False
        self.hold_token = None
        
    
    def get_next_token(self):
        
        if self.hold_token != None:
            hold = self.hold_token
            self.hold_token = None
            self.last_token = hold
            return hold
        
        c = self.reader.read(1)
        while c != None:
            token = self.tokenise_char(c)
            if token != None:
                self.last_token = token
                return token
            c = self.reader.read(1)
        return None
      
    def debug(self, msg):
        if self.debugging:
            print(msg)      
                
    def tokenise_char(self, c):
        self.pos += 1
        self.col += 1

        self.debug('TOKENISING: '+c)
        if c == '\n':
            self.debug('CR')
            self.row += 1
            self.col = 0
                    
        if self.escaping:
            self.debug('ESCAPING')
            if c == 'n':
                c = '\n'
            elif c == 'r':
                c = '\r'
            elif c == 'b' :
                c = '\b'
            elif c == 'f':
                c == '\f'
            elif c == 't':
                c = '\t'
            self.escaping = False
             
        
        if c == self.escape and self.in_quotes:
            self.debug('ESCAPE')
            self.escpaing = True
            return None
        
        if c == self.quote:
            self.debug('QUOTE')
            if self.in_quotes:
                self.token_value_quoted = True
                self.in_quotes = False
            else:
                self.in_quotes = True
            return None
        
        if self.in_quotes:
            self.debug('IN QUOTES')
            self.token_value += c
            return None
        
        if c == self.start_obj:
            self.debug('START OBJECT')
            return self.found_token(JsonNodeType.START_OBJECT)
        
        if c == self.end_obj:
            self.debug('END OBJECT')
            if self.last_token.node_type in [JsonNodeType.END_OBJECT, JsonNodeType.END_LIST]:
                return self.found_token(JsonNodeType.END_OBJECT)
            value = self.token_value
            value_quoted = self.token_value_quoted
            self.hold_token = self.found_token(JsonNodeType.END_OBJECT)
            self.token_value = value
            self.token_value_quoted = value_quoted
            
            c = self.valuesep
        
        if c == self.start_list:
            self.debug('START LIST')
            return self.found_token(JsonNodeType.START_LIST)
        
        if c == self.end_list:
            self.debug('END LIST')
            if self.last_token.node_type in [JsonNodeType.END_OBJECT, JsonNodeType.END_LIST]:
                return self.found_token(JsonNodeType.END_LIST)
            value = self.token_value
            value_quoted = self.token_value_quoted
            self.hold_token = self.found_token(JsonNodeType.END_LIST)
            self.token_value = value
            self.token_value_quoted = value_quoted
            c = self.valuesep
        
        if c == self.namesep:
            self.debug('NAMESEP')
            self.expecting_value = True
            return self.found_token(JsonNodeType.NAME, value=self.token_value)
        
        if c == self.valuesep:
            self.debug('VALUESEP')
            
            if self.token_value_quoted:
                return self.found_token(JsonNodeType.STR_VALUE, value=self.token_value)
            else:
                if numUtil.is_int(self.token_value):
                    return self.found_token(JsonNodeType.NUM_VALUE, value = int(self.token_value))
                elif numUtil.is_float(self.token_value):
                    return self.found_token(JsonNodeType.NUM_VALUE, value = float(self.token_value))
                elif self.token_value.upper() == 'NULL':
                    return self.found_token(JsonNodeType.NULL_VALUE, value=None)
                elif self.token_value.upper() == 'TRUE':
                    return self.found_token(JsonNodeType.BOOL_VALUE, value=True)
                elif self.token_value.upper() == 'FALSE':
                    return self.found_token(JsonNodeType.BOOL_VALUE, value=False)  
                return 
        
        if str(c).isspace():
            self.debug('IS SPACE')
            return
        
        self.debug('APPENDING: '+c+' to '+self.token_value)
        self.token_value += c
        return None
        
            
    def found_token(self, node_type, **kw):
        self.debug('FOUND: '+node_type.value)
        token = Token(node_type, value=kw.get('value'))
        self.token_value = ''
        self.token_value_quoted = False
        self.escaping = False
        self.in_quotes = False
        return token
    
        
        
        
        
        
        