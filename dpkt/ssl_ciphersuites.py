# Copyright 2012 Google Inc. All rights reserved.
# -*- coding: utf-8 -*-
"""
Nicely formatted cipher suite definitions for TLS

A list of cipher suites in the form of CipherSuite objects.
These are supposed to be immutable; don't mess with them.
"""


class CipherSuite(object):
    """
    Encapsulates a cipher suite.

    Members/args:
    * code: two-byte ID code, as int
    * kx: key exchange algorithm, e.g. 'RSA' or 'DHE'
    * auth: authentication algorithm, e.g. 'RSA' or 'DSS'
    * cipher: stream or block cipher algorithm, e.g. 'AES_128'
    * mode: mode of operation for block ciphers, e.g. 'CBC' or 'GCM'
    * mac: message authentication code algorithm, e.g. 'MD5' or 'SHA256'
    * name: cipher suite name as defined in the RFCs,
        e.g. 'TLS_RSA_WITH_RC4_40_MD5', can be generated by default from the
        other parameters
    * encoding: encoding algorithm, defaults to cipher+mode
    Additional members:
    * kx_auth: kx+auth algorithm, as 'KeyExchangeAlgorithm' in RFCs
    """

    def __init__(self, code, kx, auth, cipher, mode, mac, name=None, encoding=None):
        self.code = code
        # We strip trailing whitespace here because we want to format the
        # global table nicely while making pylint happy.
        self._kx = kx.rstrip()
        self._auth = auth.rstrip()
        self.cipher = cipher.rstrip()
        self.mode = mode.rstrip()
        self.mac = mac.rstrip()
        self._name = name
        self._encoding = encoding

    @property
    def kx(self):
        if self._kx == '': # for PSK
            return self._auth
        else:
            return self._kx

    @property
    def auth(self):
        if self._auth == '': # for RSA
            return self._kx
        else:
            return self._auth

    @property
    def kx_auth(self):
        if self._auth == '': # for RSA
            return self._kx
        elif self._kx == '': # for PSK
            return self._auth
        else:
            return self._kx + '_' + self._auth

    @property
    def encoding(self):
        if self._encoding is None:
            if self.mode == '':
                return self.cipher
            else:
                return self.cipher + '_' + self.mode
        else:
            return self._encoding

    @property
    def name(self):
        if self._name is None:
            if self.mac == '': # for CCM and CCM_8 modes
                return 'TLS_' + self.kx_auth + '_WITH_' + self.encoding
            else:
                return 'TLS_' + self.kx_auth + '_WITH_' + self.encoding + '_' + self.mac
        else:
            return self._name

    def __repr__(self):
        return 'CipherSuite(%s)' % self.name

    MAC_SIZES = {
        'MD5': 16,
        'SHA': 20,
        'SHA256': 32,
        'SHA384': 48,
    }

    BLOCK_SIZES = {
        '3DES_EDE': 8,
        'AES_128': 16,
        'AES_256': 16,
        'ARIA': 16,
        'CAMELLIA_128': 16,
        'CAMELLIA_256': 16,
        'CHACHA20': 64,
        'DES': 8,
        'DES40': 8,
        'IDEA': 8,
        'IDEA_128': 16,
        'RC2_40': 8,
        'RC2_128': 8,
        'RC2_128_EXPORT40': 8,
        'RC4_40': None,
        'RC4_128': None,
        'RC4_128_EXPORT40': None,
        'SEED': 16,
    }

    @property
    def mac_size(self):
        """In bytes. Default to 0."""
        return self.MAC_SIZES.get(self.mac, 0)

    @property
    def block_size(self):
        """In bytes. Default to 1."""
        return self.BLOCK_SIZES.get(self.cipher, 1)

    @property
    def pfs(self):
        return self.kx in ('DHE', 'ECDHE')

    @property
    def aead(self):
        return self.mode in ('CCM', 'CCM_8', 'GCM')

    @property
    def anonymous(self):
        return self.auth.startswith('anon')

# master list of CipherSuite Objects
# Full list from IANA:
#   https://www.iana.org/assignments/tls-parameters/tls-parameters.xhtml
CIPHERSUITES = [
    # not a real cipher suite, can be ignored, see RFC5746
    CipherSuite(0x00ff, 'NULL', '        ', 'NULL    ', '    ', 'NULL',
        'TLS_EMPTY_RENEGOTIATION_INFO'),
    # RFC7507
    CipherSuite(0x5600, '', '            ', '', '', '',
        'TLS_FALLBACK'),
    CipherSuite(0xffff, '', '            ', '', '', '',
        'UNKNOWN_CIPHER'),

    # RFC2246 : TLS 1.0
    CipherSuite(0x0000, 'NULL', '        ', 'NULL    ', '    ', 'NULL'),

    CipherSuite(0x0001, 'RSA', '         ', 'NULL    ', '    ', 'MD5'),
    CipherSuite(0x0002, 'RSA', '         ', 'NULL    ', '    ', 'SHA'),
    CipherSuite(0x0003, 'RSA_EXPORT', '  ', 'RC4_40  ', '    ', 'MD5'),
    CipherSuite(0x0004, 'RSA', '         ', 'RC4_128 ', '    ', 'MD5'),
    CipherSuite(0x0005, 'RSA', '         ', 'RC4_128 ', '    ', 'SHA'),
    CipherSuite(0x0006, 'RSA_EXPORT', '  ', 'RC2_40  ', 'CBC ', 'MD5',
        encoding='RC2_CBC_40'),
    CipherSuite(0x0007, 'RSA', '         ', 'IDEA    ', 'CBC ', 'SHA'),
    CipherSuite(0x0008, 'RSA_EXPORT', '  ', 'DES40   ', 'CBC ', 'SHA'),
    CipherSuite(0x0009, 'RSA', '         ', 'DES     ', 'CBC ', 'SHA'),
    CipherSuite(0x000a, 'RSA', '         ', '3DES_EDE', 'CBC ', 'SHA'),

    CipherSuite(0x000b, 'DH', 'DSS_EXPORT', 'DES40   ', 'CBC ', 'SHA'),
    CipherSuite(0x000c, 'DH', 'DSS       ', 'DES     ', 'CBC ', 'SHA'),
    CipherSuite(0x000d, 'DH', 'DSS       ', '3DES_EDE', 'CBC ', 'SHA'),
    CipherSuite(0x000e, 'DH', 'RSA_EXPORT', 'DES40   ', 'CBC ', 'SHA'),
    CipherSuite(0x000f, 'DH', 'RSA       ', 'DES     ', 'CBC ', 'SHA'),
    CipherSuite(0x0010, 'DH', 'RSA       ', '3DES_EDE', 'CBC ', 'SHA'),
    CipherSuite(0x0011, 'DHE', 'DSS_EXPORT','DES40   ', 'CBC ', 'SHA'),
    CipherSuite(0x0012, 'DHE', 'DSS      ', 'DES     ', 'CBC ', 'SHA'),
    CipherSuite(0x0013, 'DHE', 'DSS      ', '3DES_EDE', 'CBC ', 'SHA'),
    CipherSuite(0x0014, 'DHE', 'RSA_EXPORT','DES40   ', 'CBC ', 'SHA'),
    CipherSuite(0x0015, 'DHE', 'RSA      ', 'DES     ', 'CBC ', 'SHA'),
    CipherSuite(0x0016, 'DHE', 'RSA      ', '3DES_EDE', 'CBC ', 'SHA'),

    CipherSuite(0x0017, 'DH', 'anon_EXPORT','RC4_40  ', '    ', 'MD5'),
    CipherSuite(0x0018, 'DH', 'anon      ', 'RC4_128 ', '    ', 'MD5'),
    CipherSuite(0x0019, 'DH', 'anon_EXPORT','DES40   ', 'CBC ', 'SHA'),
    CipherSuite(0x001a, 'DH', 'anon      ', 'DES     ', 'CBC ', 'SHA'),
    CipherSuite(0x001b, 'DH', 'anon      ', '3DES_EDE', 'CBC ', 'SHA'),

    # Reserved: 0x1c-0x1d

    # RFC4346 : TLS 1.1
    # RFC2712
    CipherSuite(0x001e, 'KRB5', '        ', 'DES     ', 'CBC ', 'SHA'),
    CipherSuite(0x001f, 'KRB5', '        ', '3DES_EDE', 'CBC ', 'SHA'),
    CipherSuite(0x0020, 'KRB5', '        ', 'RC4_128 ', '    ', 'SHA'),
    CipherSuite(0x0021, 'KRB5', '        ', 'IDEA    ', 'CBC ', 'SHA'),
    CipherSuite(0x0022, 'KRB5', '        ', 'DES     ', 'CBC ', 'MD5'),
    CipherSuite(0x0023, 'KRB5', '        ', '3DES_EDE', 'CBC ', 'MD5'),
    CipherSuite(0x0024, 'KRB5', '        ', 'RC4_128 ', '    ', 'MD5'),
    CipherSuite(0x0025, 'KRB5', '        ', 'IDEA    ', 'CBC ', 'MD5'),

    CipherSuite(0x0026, 'KRB5_EXPORT', ' ', 'DES40   ', 'CBC ', 'SHA',
            encoding='DES_CBC_40'),
    CipherSuite(0x0027, 'KRB5_EXPORT', ' ', 'RC2_40  ', 'CBC ', 'SHA',
            encoding='RC2_CBC_40'),
    CipherSuite(0x0028, 'KRB5_EXPORT', ' ', 'RC4_40  ', '    ', 'SHA'),
    CipherSuite(0x0029, 'KRB5_EXPORT', ' ', 'DES40   ', 'CBC ', 'MD5',
            encoding='DES_CBC_40'),
    CipherSuite(0x002a, 'KRB5_EXPORT', ' ', 'RC2_40  ', 'CBC ', 'MD5',
            encoding='RC2_CBC_40'),
    CipherSuite(0x002b, 'KRB5_EXPORT', ' ', 'RC4_40  ', '    ', 'MD5'),

    # RFC4785
    CipherSuite(0x002c, '    ', 'PSK     ', 'NULL    ', '    ', 'SHA'),
    CipherSuite(0x002d, 'DHE ', 'PSK     ', 'NULL    ', '    ', 'SHA'),
    CipherSuite(0x002e, 'RSA ', 'PSK     ', 'NULL    ', '    ', 'SHA'),

    # RFC3268
    CipherSuite(0x002f, 'RSA ', '        ', 'AES_128 ', 'CBC ', 'SHA'),
    CipherSuite(0x0030, 'DH  ', 'DSS     ', 'AES_128 ', 'CBC ', 'SHA'),
    CipherSuite(0x0031, 'DH  ', 'RSA     ', 'AES_128 ', 'CBC ', 'SHA'),
    CipherSuite(0x0032, 'DHE ', 'DSS     ', 'AES_128 ', 'CBC ', 'SHA'),
    CipherSuite(0x0033, 'DHE ', 'RSA     ', 'AES_128 ', 'CBC ', 'SHA'),
    CipherSuite(0x0034, 'DH  ', 'anon    ', 'AES_128 ', 'CBC ', 'SHA'),

    CipherSuite(0x0035, 'RSA ', '        ', 'AES_256 ', 'CBC ', 'SHA'),
    CipherSuite(0x0036, 'DH  ', 'DSS     ', 'AES_256 ', 'CBC ', 'SHA'),
    CipherSuite(0x0037, 'DH  ', 'RSA     ', 'AES_256 ', 'CBC ', 'SHA'),
    CipherSuite(0x0038, 'DHE ', 'DSS     ', 'AES_256 ', 'CBC ', 'SHA'),
    CipherSuite(0x0039, 'DHE ', 'RSA     ', 'AES_256 ', 'CBC ', 'SHA'),
    CipherSuite(0x003a, 'DH  ', 'anon    ', 'AES_256 ', 'CBC ', 'SHA'),

    # RFC5246 : TLS 1.2
    CipherSuite(0x003b, 'RSA ', '        ', 'NULL    ', '    ', 'SHA256'),
    CipherSuite(0x003c, 'RSA ', '        ', 'AES_128 ', 'CBC ', 'SHA256'),
    CipherSuite(0x003d, 'RSA ', '        ', 'AES_256 ', 'CBC ', 'SHA256'),
    CipherSuite(0x003e, 'DH  ', 'DSS     ', 'AES_128 ', 'CBC ', 'SHA256'),
    CipherSuite(0x003f, 'DH  ', 'RSA     ', 'AES_128 ', 'CBC ', 'SHA256'),
    CipherSuite(0x0040, 'DHE ', 'DSS     ', 'AES_128 ', 'CBC ', 'SHA256'),

    # RFC5932
    CipherSuite(0x0041, 'RSA ', '        ', 'CAMELLIA_128', 'CBC', 'SHA'),
    CipherSuite(0x0042, 'DH  ', 'DSS     ', 'CAMELLIA_128', 'CBC', 'SHA'),
    CipherSuite(0x0043, 'DH  ', 'RSA     ', 'CAMELLIA_128', 'CBC', 'SHA'),
    CipherSuite(0x0044, 'DHE ', 'DSS     ', 'CAMELLIA_128', 'CBC', 'SHA'),
    CipherSuite(0x0045, 'DHE ', 'RSA     ', 'CAMELLIA_128', 'CBC', 'SHA'),
    CipherSuite(0x0046, 'DH  ', 'anon    ', 'CAMELLIA_128', 'CBC', 'SHA'),

    # Reserved: 0x47-5c
    # Unassigned: 0x5d-5f
    # Reserved: 0x60-66

    # RFC5246 : TLS 1.2
    CipherSuite(0x0067, 'DHE ', 'RSA     ', 'AES_128 ', 'CBC ', 'SHA256'),
    CipherSuite(0x0068, 'DH  ', 'DSS     ', 'AES_256 ', 'CBC ', 'SHA256'),
    CipherSuite(0x0069, 'DH  ', 'RSA     ', 'AES_256 ', 'CBC ', 'SHA256'),
    CipherSuite(0x006a, 'DHE ', 'DSS     ', 'AES_256 ', 'CBC ', 'SHA256'),
    CipherSuite(0x006b, 'DHE ', 'RSA     ', 'AES_256 ', 'CBC ', 'SHA256'),
    CipherSuite(0x006c, 'DH  ', 'anon    ', 'AES_128 ', 'CBC ', 'SHA256'),
    CipherSuite(0x006d, 'DH  ', 'anon    ', 'AES_256 ', 'CBC ', 'SHA256'),

    # Unassigned: 0x6e-83

    # RFC5932
    CipherSuite(0x0084, 'RSA ', '        ', 'CAMELLIA_256', 'CBC', 'SHA'),
    CipherSuite(0x0085, 'DH  ', 'DSS     ', 'CAMELLIA_256', 'CBC', 'SHA'),
    CipherSuite(0x0086, 'DH  ', 'RSA     ', 'CAMELLIA_256', 'CBC', 'SHA'),
    CipherSuite(0x0087, 'DHE ', 'DSS     ', 'CAMELLIA_256', 'CBC', 'SHA'),
    CipherSuite(0x0088, 'DHE ', 'RSA     ', 'CAMELLIA_256', 'CBC', 'SHA'),
    CipherSuite(0x0089, 'DH  ', 'anon    ', 'CAMELLIA_256', 'CBC', 'SHA'),

    # RFC4279
    CipherSuite(0x008a, '    ', 'PSK     ', 'RC4_128 ', '    ', 'SHA'),
    CipherSuite(0x008b, '    ', 'PSK     ', '3DES_EDE', 'CBC ', 'SHA'),
    CipherSuite(0x008c, '    ', 'PSK     ', 'AES_128 ', 'CBC ', 'SHA'),
    CipherSuite(0x008d, '    ', 'PSK     ', 'AES_256 ', 'CBC ', 'SHA'),
    CipherSuite(0x008e, 'DHE ', 'PSK     ', 'RC4_128 ', '    ', 'SHA'),
    CipherSuite(0x008f, 'DHE ', 'PSK     ', '3DES_EDE', 'CBC ', 'SHA'),
    CipherSuite(0x0090, 'DHE ', 'PSK     ', 'AES_128 ', 'CBC ', 'SHA'),
    CipherSuite(0x0091, 'DHE ', 'PSK     ', 'AES_256 ', 'CBC ', 'SHA'),
    CipherSuite(0x0092, 'RSA ', 'PSK     ', 'RC4_128 ', '    ', 'SHA'),
    CipherSuite(0x0093, 'RSA ', 'PSK     ', '3DES_EDE', 'CBC ', 'SHA'),
    CipherSuite(0x0094, 'RSA ', 'PSK     ', 'AES_128 ', 'CBC ', 'SHA'),
    CipherSuite(0x0095, 'RSA ', 'PSK     ', 'AES_256 ', 'CBC ', 'SHA'),

    # RFC4162
    CipherSuite(0x0096, 'RSA ', '        ', 'SEED    ', 'CBC ', 'SHA'),
    CipherSuite(0x0097, 'DH  ', 'DSS     ', 'SEED    ', 'CBC ', 'SHA'),
    CipherSuite(0x0098, 'DH  ', 'RSA     ', 'SEED    ', 'CBC ', 'SHA'),
    CipherSuite(0x0099, 'DHE ', 'DSS     ', 'SEED    ', 'CBC ', 'SHA'),
    CipherSuite(0x009a, 'DHE ', 'RSA     ', 'SEED    ', 'CBC ', 'SHA'),
    CipherSuite(0x009b, 'DH  ', 'anon    ', 'SEED    ', 'CBC ', 'SHA'),

    # RFC5288
    CipherSuite(0x009c, 'RSA ', '        ', 'AES_128 ', 'GCM ', 'SHA256'),
    CipherSuite(0x009d, 'RSA ', '        ', 'AES_256 ', 'GCM ', 'SHA384'),
    CipherSuite(0x009e, 'DHE ', 'RSA     ', 'AES_128 ', 'GCM ', 'SHA256'),
    CipherSuite(0x009f, 'DHE ', 'RSA     ', 'AES_256 ', 'GCM ', 'SHA384'),
    CipherSuite(0x00a0, 'DH  ', 'RSA     ', 'AES_128 ', 'GCM ', 'SHA256'),
    CipherSuite(0x00a1, 'DH  ', 'RSA     ', 'AES_256 ', 'GCM ', 'SHA384'),
    CipherSuite(0x00a2, 'DHE ', 'DSS     ', 'AES_128 ', 'GCM ', 'SHA256'),
    CipherSuite(0x00a3, 'DHE ', 'DSS     ', 'AES_256 ', 'GCM ', 'SHA384'),
    CipherSuite(0x00a4, 'DH  ', 'DSS     ', 'AES_128 ', 'GCM ', 'SHA256'),
    CipherSuite(0x00a5, 'DH  ', 'DSS     ', 'AES_256 ', 'GCM ', 'SHA384'),
    CipherSuite(0x00a6, 'DH  ', 'anon    ', 'AES_128 ', 'GCM ', 'SHA256'),
    CipherSuite(0x00a7, 'DH  ', 'anon    ', 'AES_256 ', 'GCM ', 'SHA384'),

    # RFC5487
    CipherSuite(0x00a8, '    ', 'PSK     ', 'AES_128 ', 'GCM ', 'SHA256'),
    CipherSuite(0x00a9, '    ', 'PSK     ', 'AES_256 ', 'GCM ', 'SHA384'),
    CipherSuite(0x00aa, 'DHE ', 'PSK     ', 'AES_128 ', 'GCM ', 'SHA256'),
    CipherSuite(0x00ab, 'DHE ', 'PSK     ', 'AES_256 ', 'GCM ', 'SHA384'),
    CipherSuite(0x00ac, 'RSA ', 'PSK     ', 'AES_128 ', 'GCM ', 'SHA256'),
    CipherSuite(0x00ad, 'RSA ', 'PSK     ', 'AES_256 ', 'GCM ', 'SHA384'),

    CipherSuite(0x00ae, '    ', 'PSK     ', 'AES_128 ', 'CBC ', 'SHA256'),
    CipherSuite(0x00af, '    ', 'PSK     ', 'AES_256 ', 'CBC ', 'SHA384'),
    CipherSuite(0x00b0, '    ', 'PSK     ', 'NULL    ', '    ', 'SHA256'),
    CipherSuite(0x00b1, '    ', 'PSK     ', 'NULL    ', '    ', 'SHA384'),

    CipherSuite(0x00b2, 'DHE ', 'PSK     ', 'AES_128 ', 'CBC ', 'SHA256'),
    CipherSuite(0x00b3, 'DHE ', 'PSK     ', 'AES_256 ', 'CBC ', 'SHA384'),
    CipherSuite(0x00b4, 'DHE ', 'PSK     ', 'NULL    ', '    ', 'SHA256'),
    CipherSuite(0x00b5, 'DHE ', 'PSK     ', 'NULL    ', '    ', 'SHA384'),

    CipherSuite(0x00b6, 'RSA ', 'PSK     ', 'AES_128 ', 'CBC ', 'SHA256'),
    CipherSuite(0x00b7, 'RSA ', 'PSK     ', 'AES_256 ', 'CBC ', 'SHA384'),
    CipherSuite(0x00b8, 'RSA ', 'PSK     ', 'NULL    ', '    ', 'SHA256'),
    CipherSuite(0x00b9, 'RSA ', 'PSK     ', 'NULL    ', '    ', 'SHA384'),

    # RFC5932
    CipherSuite(0x00ba, 'RSA ', '        ', 'CAMELLIA_128', 'CBC', 'SHA256'),
    CipherSuite(0x00bb, 'DH  ', 'DSS     ', 'CAMELLIA_128', 'CBC', 'SHA256'),
    CipherSuite(0x00bc, 'DH  ', 'RSA     ', 'CAMELLIA_128', 'CBC', 'SHA256'),
    CipherSuite(0x00bd, 'DHE ', 'DSS     ', 'CAMELLIA_128', 'CBC', 'SHA256'),
    CipherSuite(0x00be, 'DHE ', 'RSA     ', 'CAMELLIA_128', 'CBC', 'SHA256'),
    CipherSuite(0x00bf, 'DH  ', 'anon    ', 'CAMELLIA_128', 'CBC', 'SHA256'),

    CipherSuite(0x00c0, 'RSA ', '        ', 'CAMELLIA_256', 'CBC', 'SHA256'),
    CipherSuite(0x00c1, 'DH  ', 'DSS     ', 'CAMELLIA_256', 'CBC', 'SHA256'),
    CipherSuite(0x00c2, 'DH  ', 'RSA     ', 'CAMELLIA_256', 'CBC', 'SHA256'),
    CipherSuite(0x00c3, 'DHE ', 'DSS     ', 'CAMELLIA_256', 'CBC', 'SHA256'),
    CipherSuite(0x00c4, 'DHE ', 'RSA     ', 'CAMELLIA_256', 'CBC', 'SHA256'),
    CipherSuite(0x00c5, 'DH  ', 'anon    ', 'CAMELLIA_256', 'CBC', 'SHA256'),

    # RFC4492
    CipherSuite(0xc001, 'ECDH ', 'ECDSA  ', 'NULL    ', '    ', 'SHA'),
    CipherSuite(0xc002, 'ECDH ', 'ECDSA  ', 'RC4_128 ', '    ', 'SHA'),
    CipherSuite(0xc003, 'ECDH ', 'ECDSA  ', '3DES_EDE', 'CBC ', 'SHA'),
    CipherSuite(0xc004, 'ECDH ', 'ECDSA  ', 'AES_128 ', 'CBC ', 'SHA'),
    CipherSuite(0xc005, 'ECDH ', 'ECDSA  ', 'AES_256 ', 'CBC ', 'SHA'),

    CipherSuite(0xc006, 'ECDHE', 'ECDSA  ', 'NULL    ', '    ', 'SHA'),
    CipherSuite(0xc007, 'ECDHE', 'ECDSA  ', 'RC4_128 ', '    ', 'SHA'),
    CipherSuite(0xc008, 'ECDHE', 'ECDSA  ', '3DES_EDE', 'CBC ', 'SHA'),
    CipherSuite(0xc009, 'ECDHE', 'ECDSA  ', 'AES_128 ', 'CBC ', 'SHA'),
    CipherSuite(0xc00a, 'ECDHE', 'ECDSA  ', 'AES_256 ', 'CBC ', 'SHA'),

    CipherSuite(0xc00b, 'ECDH ', 'RSA    ', 'NULL    ', '    ', 'SHA'),
    CipherSuite(0xc00c, 'ECDH ', 'RSA    ', 'RC4_128 ', '    ', 'SHA'),
    CipherSuite(0xc00d, 'ECDH ', 'RSA    ', '3DES_EDE', 'CBC ', 'SHA'),
    CipherSuite(0xc00e, 'ECDH ', 'RSA    ', 'AES_128 ', 'CBC ', 'SHA'),
    CipherSuite(0xc00f, 'ECDH ', 'RSA    ', 'AES_256 ', 'CBC ', 'SHA'),

    CipherSuite(0xc010, 'ECDHE', 'RSA    ', 'NULL    ', '    ', 'SHA'),
    CipherSuite(0xc011, 'ECDHE', 'RSA    ', 'RC4_128 ', '    ', 'SHA'),
    CipherSuite(0xc012, 'ECDHE', 'RSA    ', '3DES_EDE', 'CBC ', 'SHA'),
    CipherSuite(0xc013, 'ECDHE', 'RSA    ', 'AES_128 ', 'CBC ', 'SHA'),
    CipherSuite(0xc014, 'ECDHE', 'RSA    ', 'AES_256 ', 'CBC ', 'SHA'),

    CipherSuite(0xc015, 'ECDH ', 'anon   ', 'NULL    ', '    ', 'SHA'),
    CipherSuite(0xc016, 'ECDH ', 'anon   ', 'RC4_128 ', '    ', 'SHA'),
    CipherSuite(0xc017, 'ECDH ', 'anon   ', '3DES_EDE', 'CBC ', 'SHA'),
    CipherSuite(0xc018, 'ECDH ', 'anon   ', 'AES_128 ', 'CBC ', 'SHA'),
    CipherSuite(0xc019, 'ECDH ', 'anon   ', 'AES_256 ', 'CBC ', 'SHA'),

    # RFC5054
    CipherSuite(0xc01a, 'SRP_SHA', '     ', '3DES_EDE', 'CBC ', 'SHA'),
    CipherSuite(0xc01b, 'SRP_SHA', 'RSA  ', '3DES_EDE', 'CBC ', 'SHA'),
    CipherSuite(0xc01c, 'SRP_SHA', 'DSS  ', '3DES_EDE', 'CBC ', 'SHA'),
    CipherSuite(0xc01d, 'SRP_SHA', '     ', 'AES_128 ', 'CBC ', 'SHA'),
    CipherSuite(0xc01e, 'SRP_SHA', 'RSA  ', 'AES_128 ', 'CBC ', 'SHA'),
    CipherSuite(0xc01f, 'SRP_SHA', 'DSS  ', 'AES_128 ', 'CBC ', 'SHA'),
    CipherSuite(0xc020, 'SRP_SHA', '     ', 'AES_256 ', 'CBC ', 'SHA'),
    CipherSuite(0xc021, 'SRP_SHA', 'RSA  ', 'AES_256 ', 'CBC ', 'SHA'),
    CipherSuite(0xc022, 'SRP_SHA', 'DSS  ', 'AES_256 ', 'CBC ', 'SHA'),

    # RFC5289
    CipherSuite(0xc023, 'ECDHE', 'ECDSA  ', 'AES_128 ', 'CBC ', 'SHA256'),
    CipherSuite(0xc024, 'ECDHE', 'ECDSA  ', 'AES_256 ', 'CBC ', 'SHA384'),
    CipherSuite(0xc025, 'ECDH ', 'ECDSA  ', 'AES_128 ', 'CBC ', 'SHA256'),
    CipherSuite(0xc026, 'ECDH ', 'ECDSA  ', 'AES_256 ', 'CBC ', 'SHA384'),
    CipherSuite(0xc027, 'ECDHE', 'RSA    ', 'AES_128 ', 'CBC ', 'SHA256'),
    CipherSuite(0xc028, 'ECDHE', 'RSA    ', 'AES_256 ', 'CBC ', 'SHA384'),
    CipherSuite(0xc029, 'ECDH ', 'RSA    ', 'AES_128 ', 'CBC ', 'SHA256'),
    CipherSuite(0xc02a, 'ECDH ', 'RSA    ', 'AES_256 ', 'CBC ', 'SHA384'),

    CipherSuite(0xc02b, 'ECDHE', 'ECDSA  ', 'AES_128 ', 'GCM ', 'SHA256'),
    CipherSuite(0xc02c, 'ECDHE', 'ECDSA  ', 'AES_256 ', 'GCM ', 'SHA384'),
    CipherSuite(0xc02d, 'ECDH ', 'ECDSA  ', 'AES_128 ', 'GCM ', 'SHA256'),
    CipherSuite(0xc02e, 'ECDH ', 'ECDSA  ', 'AES_256 ', 'GCM ', 'SHA384'),
    CipherSuite(0xc02f, 'ECDHE', 'RSA    ', 'AES_128 ', 'GCM ', 'SHA256'),
    CipherSuite(0xc030, 'ECDHE', 'RSA    ', 'AES_256 ', 'GCM ', 'SHA384'),
    CipherSuite(0xc031, 'ECDH ', 'RSA    ', 'AES_128 ', 'GCM ', 'SHA256'),
    CipherSuite(0xc032, 'ECDH ', 'RSA    ', 'AES_256 ', 'GCM ', 'SHA384'),

    # RFC5489
    CipherSuite(0xc033, 'ECDHE', 'PSK    ', 'RC4_128 ', '    ', 'SHA'),
    CipherSuite(0xc034, 'ECDHE', 'PSK    ', '3DES_EDE', 'CBC ', 'SHA'),
    CipherSuite(0xc035, 'ECDHE', 'PSK    ', 'AES_128 ', 'CBC ', 'SHA'),
    CipherSuite(0xc036, 'ECDHE', 'PSK    ', 'AES_256 ', 'CBC ', 'SHA'),
    CipherSuite(0xc037, 'ECDHE', 'PSK    ', 'AES_128 ', 'CBC ', 'SHA256'),
    CipherSuite(0xc038, 'ECDHE', 'PSK    ', 'AES_256 ', 'CBC ', 'SHA384'),
    CipherSuite(0xc039, 'ECDHE', 'PSK    ', 'NULL    ', '    ', 'SHA'),
    CipherSuite(0xc03a, 'ECDHE', 'PSK    ', 'NULL    ', '    ', 'SHA256'),
    CipherSuite(0xc03b, 'ECDHE', 'PSK    ', 'NULL    ', '    ', 'SHA384'),

    # RFC6209
    CipherSuite(0xc03c, 'RSA ', '        ', 'ARIA_128', 'CBC ', 'SHA256'),
    CipherSuite(0xc03d, 'RSA ', '        ', 'ARIA_256', 'CBC ', 'SHA384'),
    CipherSuite(0xc03e, 'DH  ', 'DSS     ', 'ARIA_128', 'CBC ', 'SHA256'),
    CipherSuite(0xc03f, 'DH  ', 'DSS     ', 'ARIA_256', 'CBC ', 'SHA384'),
    CipherSuite(0xc040, 'DH  ', 'RSA     ', 'ARIA_128', 'CBC ', 'SHA256'),
    CipherSuite(0xc041, 'DH  ', 'RSA     ', 'ARIA_256', 'CBC ', 'SHA384'),
    CipherSuite(0xc042, 'DHE ', 'DSS     ', 'ARIA_128', 'CBC ', 'SHA256'),
    CipherSuite(0xc043, 'DHE ', 'DSS     ', 'ARIA_256', 'CBC ', 'SHA384'),
    CipherSuite(0xc044, 'DHE ', 'RSA     ', 'ARIA_128', 'CBC ', 'SHA256'),
    CipherSuite(0xc045, 'DHE ', 'RSA     ', 'ARIA_256', 'CBC ', 'SHA384'),
    CipherSuite(0xc046, 'DH  ', 'anon    ', 'ARIA_128', 'CBC ', 'SHA256'),
    CipherSuite(0xc047, 'DH  ', 'anon    ', 'ARIA_256', 'CBC ', 'SHA384'),

    CipherSuite(0xc048, 'ECDHE', 'ECDSA  ', 'ARIA_128', 'CBC ', 'SHA256'),
    CipherSuite(0xc049, 'ECDHE', 'ECDSA  ', 'ARIA_256', 'CBC ', 'SHA384'),
    CipherSuite(0xc04a, 'ECDH ', 'ECDSA  ', 'ARIA_128', 'CBC ', 'SHA256'),
    CipherSuite(0xc04b, 'ECDH ', 'ECDSA  ', 'ARIA_256', 'CBC ', 'SHA384'),
    CipherSuite(0xc04c, 'ECDHE', 'RSA    ', 'ARIA_128', 'CBC ', 'SHA256'),
    CipherSuite(0xc04d, 'ECDHE', 'RSA    ', 'ARIA_256', 'CBC ', 'SHA384'),
    CipherSuite(0xc04e, 'ECDH ', 'RSA    ', 'ARIA_128', 'CBC ', 'SHA256'),
    CipherSuite(0xc04f, 'ECDH ', 'RSA    ', 'ARIA_256', 'CBC ', 'SHA384'),

    CipherSuite(0xc050, 'RSA ', '        ', 'ARIA_128', 'GCM ', 'SHA256'),
    CipherSuite(0xc051, 'RSA ', '        ', 'ARIA_256', 'GCM ', 'SHA384'),
    CipherSuite(0xc052, 'DHE ', 'RSA     ', 'ARIA_128', 'GCM ', 'SHA256'),
    CipherSuite(0xc053, 'DHE ', 'RSA     ', 'ARIA_256', 'GCM ', 'SHA384'),
    CipherSuite(0xc054, 'DH  ', 'RSA     ', 'ARIA_128', 'GCM ', 'SHA256'),
    CipherSuite(0xc055, 'DH  ', 'RSA     ', 'ARIA_256', 'GCM ', 'SHA384'),
    CipherSuite(0xc056, 'DHE ', 'DSS     ', 'ARIA_128', 'GCM ', 'SHA256'),
    CipherSuite(0xc057, 'DHE ', 'DSS     ', 'ARIA_256', 'GCM ', 'SHA384'),
    CipherSuite(0xc058, 'DH  ', 'DSS     ', 'ARIA_128', 'GCM ', 'SHA256'),
    CipherSuite(0xc059, 'DH  ', 'DSS     ', 'ARIA_256', 'GCM ', 'SHA384'),
    CipherSuite(0xc05a, 'DH  ', 'anon    ', 'ARIA_128', 'GCM ', 'SHA256'),
    CipherSuite(0xc05b, 'DH  ', 'anon    ', 'ARIA_256', 'GCM ', 'SHA384'),

    CipherSuite(0xc05c, 'ECDHE', 'ECDSA  ', 'ARIA_128', 'GCM ', 'SHA256'),
    CipherSuite(0xc05d, 'ECDHE', 'ECDSA  ', 'ARIA_256', 'GCM ', 'SHA384'),
    CipherSuite(0xc05e, 'ECDH ', 'ECDSA  ', 'ARIA_128', 'GCM ', 'SHA256'),
    CipherSuite(0xc05f, 'ECDH ', 'ECDSA  ', 'ARIA_256', 'GCM ', 'SHA384'),
    CipherSuite(0xc060, 'ECDHE', 'RSA    ', 'ARIA_128', 'GCM ', 'SHA256'),
    CipherSuite(0xc061, 'ECDHE', 'RSA    ', 'ARIA_256', 'GCM ', 'SHA384'),
    CipherSuite(0xc062, 'ECDH ', 'RSA    ', 'ARIA_128', 'GCM ', 'SHA256'),
    CipherSuite(0xc063, 'ECDH ', 'RSA    ', 'ARIA_256', 'GCM ', 'SHA384'),

    CipherSuite(0xc064, '    ', 'PSK     ', 'ARIA_128', 'CBC ', 'SHA256'),
    CipherSuite(0xc065, '    ', 'PSK     ', 'ARIA_256', 'CBC ', 'SHA384'),
    CipherSuite(0xc066, 'DHE ', 'PSK     ', 'ARIA_128', 'CBC ', 'SHA256'),
    CipherSuite(0xc067, 'DHE ', 'PSK     ', 'ARIA_256', 'CBC ', 'SHA384'),
    CipherSuite(0xc068, 'RSA ', 'PSK     ', 'ARIA_128', 'CBC ', 'SHA256'),
    CipherSuite(0xc069, 'RSA ', 'PSK     ', 'ARIA_256', 'CBC ', 'SHA384'),
    CipherSuite(0xc06a, '    ', 'PSK     ', 'ARIA_128', 'GCM ', 'SHA256'),
    CipherSuite(0xc06b, '    ', 'PSK     ', 'ARIA_256', 'GCM ', 'SHA384'),
    CipherSuite(0xc06c, 'DHE ', 'PSK     ', 'ARIA_128', 'GCM ', 'SHA256'),
    CipherSuite(0xc06d, 'DHE ', 'PSK     ', 'ARIA_256', 'GCM ', 'SHA384'),
    CipherSuite(0xc06e, 'RSA ', 'PSK     ', 'ARIA_128', 'GCM ', 'SHA256'),
    CipherSuite(0xc06f, 'RSA ', 'PSK     ', 'ARIA_256', 'GCM ', 'SHA384'),
    CipherSuite(0xc070, 'ECDHE', 'PSK    ', 'ARIA_128', 'GCM ', 'SHA256'),
    CipherSuite(0xc071, 'ECDHE', 'PSK    ', 'ARIA_256', 'GCM ', 'SHA384'),

    # RFC6367
    CipherSuite(0xc072, 'ECDHE', 'ECDSA  ', 'CAMELLIA_128', 'CBC', 'SHA256'),
    CipherSuite(0xc073, 'ECDHE', 'ECDSA  ', 'CAMELLIA_256', 'CBC', 'SHA384'),
    CipherSuite(0xc074, 'ECDH ', 'ECDSA  ', 'CAMELLIA_128', 'CBC', 'SHA256'),
    CipherSuite(0xc075, 'ECDH ', 'ECDSA  ', 'CAMELLIA_256', 'CBC', 'SHA384'),
    CipherSuite(0xc076, 'ECDHE', 'RSA    ', 'CAMELLIA_128', 'CBC', 'SHA256'),
    CipherSuite(0xc077, 'ECDHE', 'RSA    ', 'CAMELLIA_256', 'CBC', 'SHA384'),
    CipherSuite(0xc078, 'ECDH ', 'RSA    ', 'CAMELLIA_128', 'CBC', 'SHA256'),
    CipherSuite(0xc079, 'ECDH ', 'RSA    ', 'CAMELLIA_256', 'CBC', 'SHA384'),

    CipherSuite(0xc07a, 'RSA ', '        ', 'CAMELLIA_128', 'GCM', 'SHA256'),
    CipherSuite(0xc07b, 'RSA ', '        ', 'CAMELLIA_256', 'GCM', 'SHA384'),
    CipherSuite(0xc07c, 'DHE ', 'RSA     ', 'CAMELLIA_128', 'GCM', 'SHA256'),
    CipherSuite(0xc07d, 'DHE ', 'RSA     ', 'CAMELLIA_256', 'GCM', 'SHA384'),
    CipherSuite(0xc07e, 'DH  ', 'RSA     ', 'CAMELLIA_128', 'GCM', 'SHA256'),
    CipherSuite(0xc07f, 'DH  ', 'RSA     ', 'CAMELLIA_256', 'GCM', 'SHA384'),
    CipherSuite(0xc080, 'DHE ', 'DSS     ', 'CAMELLIA_128', 'GCM', 'SHA256'),
    CipherSuite(0xc081, 'DHE ', 'DSS     ', 'CAMELLIA_256', 'GCM', 'SHA384'),
    CipherSuite(0xc082, 'DH  ', 'DSS     ', 'CAMELLIA_128', 'GCM', 'SHA256'),
    CipherSuite(0xc083, 'DH  ', 'DSS     ', 'CAMELLIA_256', 'GCM', 'SHA384'),
    CipherSuite(0xc084, 'DH  ', 'anon    ', 'CAMELLIA_128', 'GCM', 'SHA256'),
    CipherSuite(0xc085, 'DH  ', 'anon    ', 'CAMELLIA_256', 'GCM', 'SHA384'),

    CipherSuite(0xc086, 'ECDHE', 'ECDSA  ', 'CAMELLIA_128', 'GCM', 'SHA256'),
    CipherSuite(0xc087, 'ECDHE', 'ECDSA  ', 'CAMELLIA_256', 'GCM', 'SHA384'),
    CipherSuite(0xc088, 'ECDH ', 'ECDSA  ', 'CAMELLIA_128', 'GCM', 'SHA256'),
    CipherSuite(0xc089, 'ECDH ', 'ECDSA  ', 'CAMELLIA_256', 'GCM', 'SHA384'),
    CipherSuite(0xc08a, 'ECDHE', 'RSA    ', 'CAMELLIA_128', 'GCM', 'SHA256'),
    CipherSuite(0xc08b, 'ECDHE', 'RSA    ', 'CAMELLIA_256', 'GCM', 'SHA384'),
    CipherSuite(0xc08c, 'ECDH ', 'RSA    ', 'CAMELLIA_128', 'GCM', 'SHA256'),
    CipherSuite(0xc08d, 'ECDH ', 'RSA    ', 'CAMELLIA_256', 'GCM', 'SHA384'),

    CipherSuite(0xc08e, '    ', 'PSK     ', 'CAMELLIA_128', 'GCM', 'SHA256'),
    CipherSuite(0xc08f, '    ', 'PSK     ', 'CAMELLIA_256', 'GCM', 'SHA384'),
    CipherSuite(0xc090, 'DHE ', 'PSK     ', 'CAMELLIA_128', 'GCM', 'SHA256'),
    CipherSuite(0xc091, 'DHE ', 'PSK     ', 'CAMELLIA_256', 'GCM', 'SHA384'),
    CipherSuite(0xc092, 'RSA ', 'PSK     ', 'CAMELLIA_128', 'GCM', 'SHA256'),
    CipherSuite(0xc093, 'RSA ', 'PSK     ', 'CAMELLIA_256', 'GCM', 'SHA384'),
    CipherSuite(0xc094, '    ', 'PSK     ', 'CAMELLIA_128', 'CBC', 'SHA256'),
    CipherSuite(0xc095, '    ', 'PSK     ', 'CAMELLIA_256', 'CBC', 'SHA384'),
    CipherSuite(0xc096, 'DHE ', 'PSK     ', 'CAMELLIA_128', 'CBC', 'SHA256'),
    CipherSuite(0xc097, 'DHE ', 'PSK     ', 'CAMELLIA_256', 'CBC', 'SHA384'),
    CipherSuite(0xc098, 'RSA ', 'PSK     ', 'CAMELLIA_128', 'CBC', 'SHA256'),
    CipherSuite(0xc099, 'RSA ', 'PSK     ', 'CAMELLIA_256', 'CBC', 'SHA384'),
    CipherSuite(0xc09a, 'ECDHE', 'PSK    ', 'CAMELLIA_128', 'CBC', 'SHA256'),
    CipherSuite(0xc09b, 'ECDHE', 'PSK    ', 'CAMELLIA_256', 'CBC', 'SHA384'),

    # RFC6655
    CipherSuite(0xc09c, 'RSA ', '        ', 'AES_128 ', 'CCM ', ''),
    CipherSuite(0xc09d, 'RSA ', '        ', 'AES_256 ', 'CCM ', ''),
    CipherSuite(0xc09e, 'DHE ', 'RSA     ', 'AES_128 ', 'CCM ', ''),
    CipherSuite(0xc09f, 'DHE ', 'RSA     ', 'AES_256 ', 'CCM ', ''),
    CipherSuite(0xc0a0, 'RSA ', '        ', 'AES_128 ', 'CCM_8', ''),
    CipherSuite(0xc0a1, 'RSA ', '        ', 'AES_256 ', 'CCM_8', ''),
    CipherSuite(0xc0a2, 'DHE ', 'RSA     ', 'AES_128 ', 'CCM_8', ''),
    CipherSuite(0xc0a3, 'DHE ', 'RSA     ', 'AES_256 ', 'CCM_8', ''),

    CipherSuite(0xc0a4, '    ', 'PSK     ', 'AES_128 ', 'CCM ', ''),
    CipherSuite(0xc0a5, '    ', 'PSK     ', 'AES_256 ', 'CCM ', ''),
    CipherSuite(0xc0a6, 'DHE ', 'PSK     ', 'AES_128 ', 'CCM ', ''),
    CipherSuite(0xc0a7, 'DHE ', 'PSK     ', 'AES_256 ', 'CCM ', ''),
    CipherSuite(0xc0a8, '    ', 'PSK     ', 'AES_128 ', 'CCM_8', ''),
    CipherSuite(0xc0a9, '    ', 'PSK     ', 'AES_256 ', 'CCM_8', ''),
    CipherSuite(0xc0aa, 'DHE ', 'PSK     ', 'AES_128 ', 'CCM_8', ''),
    CipherSuite(0xc0ab, 'DHE ', 'PSK     ', 'AES_256 ', 'CCM_8', ''),

    # RFC7251
    CipherSuite(0xc0ac, 'ECDHE', 'ECDSA  ', 'AES_128 ', 'CCM ', ''),
    CipherSuite(0xc0ad, 'ECDHE', 'ECDSA  ', 'AES_256 ', 'CCM ', ''),
    CipherSuite(0xc0ae, 'ECDHE', 'ECDSA  ', 'AES_128 ', 'CCM_8', ''),
    CipherSuite(0xc0af, 'ECDHE', 'ECDSA  ', 'AES_256 ', 'CCM_8', ''),

    # Unassigned: 0xc0b0-0xcca7
    CipherSuite(0xcc13, 'ECDHE', 'RSA    ', 'CHACHA20', 'POLY1305', 'SHA256',
        'OLD_TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256'),
    CipherSuite(0xcc14, 'ECDHE', 'ECDSA  ', 'CHACHA20', 'POLY1305', 'SHA256',
        'OLD_TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256'),
    CipherSuite(0xcc15, 'DHE  ', 'RSA    ', 'CHACHA20', 'POLY1305', 'SHA256',
        'OLD_TLS_DHE_RSA_WITH_CHACHA20_POLY1305_SHA256'),

    # RFC7905
    CipherSuite(0xcca8, 'ECDHE', 'RSA    ', 'CHACHA20', 'POLY1305', 'SHA256'),
    CipherSuite(0xcca9, 'ECDHE', 'ECDSA  ', 'CHACHA20', 'POLY1305', 'SHA256'),
    CipherSuite(0xccaa, 'DHE  ', 'RSA    ', 'CHACHA20', 'POLY1305', 'SHA256'),

    CipherSuite(0xccab, '     ', 'PSK    ', 'CHACHA20', 'POLY1305', 'SHA256'),
    CipherSuite(0xccac, 'ECDHE', 'PSK    ', 'CHACHA20', 'POLY1305', 'SHA256'),
    CipherSuite(0xccad, 'DHE  ', 'PSK    ', 'CHACHA20', 'POLY1305', 'SHA256'),
    CipherSuite(0xccae, 'RSA  ', 'PSK    ', 'CHACHA20', 'POLY1305', 'SHA256'),

    # Unassigned: 0xccaf-0xfefd
    # Reserved: 0xfefe-0xffff

    CipherSuite(0x010080, 'RSA', 'RSA    ', 'RC4_128         ', '   ', 'MD5',
            'SSL_CK_RC4_128_WITH_MD5'),
    CipherSuite(0x020080, 'RSA', 'RSA    ', 'RC4_128_EXPORT40', '   ', 'MD5',
            'SSL_CK_RC4_128_EXPORT40_WITH_MD5'),
    CipherSuite(0x030080, 'RSA', 'RSA    ', 'RC2_128         ', 'CBC', 'MD5',
            'SSL_CK_RC2_128_CBC_WITH_MD5',          'RC2_CBC_128'),
    CipherSuite(0x040080, 'RSA', 'RSA    ', 'RC2_128_EXPORT40', 'CBC', 'MD5',
            'SSL_CK_RC2_128_CBC_EXPORT40_WITH_MD5', 'RC2_CBC_128_EXPORT40'),
    CipherSuite(0x050080, 'RSA', 'RSA    ', 'IDEA_128        ', 'CBC', 'MD5',
            'SSL_CK_IDEA_128_CBC_WITH_MD5',         'IDEA_CBC_128'),
    CipherSuite(0x060040, 'RSA', 'RSA    ', 'DES             ', 'CBC', 'MD5',
            'SSL_CK_DES_64_CBC_WITH_MD5',           'DES_CBC_64'),
    CipherSuite(0x0700C0, 'RSA', 'RSA    ', '3DES            ', 'CBC', 'MD5',
            'SSL_CK_DES_192_EDE3_CBC_WITH_MD5',     'DES_EDE3_CBC_192'),
]

BY_CODE = dict(
    (cipher.code, cipher) for cipher in CIPHERSUITES)

# This is a function to avoid artificially increased coverage
BY_NAME_DICT = None
def BY_NAME(name):
    # We initialize the dictionary only on the first call
    global BY_NAME_DICT
    if BY_NAME_DICT is None:
        BY_NAME_DICT = dict((suite.name, suite) for suite in CIPHERSUITES)
    return BY_NAME_DICT[name]

NULL_SUITE = BY_CODE[0x0000]


class TestCipherSuites(object):

    def test_kx(self):
        # A test from each RFC
        assert (BY_CODE[0x0005].kx == 'RSA')
        assert (BY_CODE[0x0021].kx == 'KRB5')
        assert (BY_CODE[0x002d].kx == 'DHE')
        assert (BY_CODE[0x0034].kx == 'DH')
        assert (BY_CODE[0x003c].kx == 'RSA')
        assert (BY_CODE[0x0042].kx == 'DH')
        assert (BY_CODE[0x006a].kx == 'DHE')
        assert (BY_CODE[0x0084].kx == 'RSA')
        assert (BY_CODE[0x0091].kx == 'DHE')
        assert (BY_CODE[0x0098].kx == 'DH')
        assert (BY_CODE[0x00ab].kx == 'DHE')
        assert (BY_CODE[0x00b0].kx == 'PSK')
        assert (BY_CODE[0x00bb].kx == 'DH')
        assert (BY_CODE[0xc008].kx == 'ECDHE')
        assert (BY_CODE[0xc016].kx == 'ECDH')
        assert (BY_CODE[0xc01d].kx == 'SRP_SHA')
        assert (BY_CODE[0xc027].kx == 'ECDHE')
        assert (BY_CODE[0xc036].kx == 'ECDHE')
        assert (BY_CODE[0xc045].kx == 'DHE')
        assert (BY_CODE[0xc052].kx == 'DHE')
        assert (BY_CODE[0xc068].kx == 'RSA')
        assert (BY_CODE[0xc074].kx == 'ECDH')
        assert (BY_CODE[0xc08d].kx == 'ECDH')
        assert (BY_CODE[0xc09d].kx == 'RSA')
        assert (BY_CODE[0xc0a2].kx == 'DHE')
        assert (BY_CODE[0xc0ad].kx == 'ECDHE')
        assert (BY_CODE[0xcc13].kx == 'ECDHE')
        assert (BY_CODE[0xcca8].kx == 'ECDHE')
        assert (BY_CODE[0xccae].kx == 'RSA')

    def test_auth(self):
        # A test from each RFC
        assert (BY_CODE[0x0005].auth == 'RSA')
        assert (BY_CODE[0x0021].auth == 'KRB5')
        assert (BY_CODE[0x002d].auth == 'PSK')
        assert (BY_CODE[0x0034].auth == 'anon')
        assert (BY_CODE[0x003c].auth == 'RSA')
        assert (BY_CODE[0x0042].auth == 'DSS')
        assert (BY_CODE[0x006a].auth == 'DSS')
        assert (BY_CODE[0x0084].auth == 'RSA')
        assert (BY_CODE[0x0091].auth == 'PSK')
        assert (BY_CODE[0x0098].auth == 'RSA')
        assert (BY_CODE[0x00ab].auth == 'PSK')
        assert (BY_CODE[0x00b0].auth == 'PSK')
        assert (BY_CODE[0x00bb].auth == 'DSS')
        assert (BY_CODE[0xc008].auth == 'ECDSA')
        assert (BY_CODE[0xc016].auth == 'anon')
        assert (BY_CODE[0xc01d].auth == 'SRP_SHA')
        assert (BY_CODE[0xc027].auth == 'RSA')
        assert (BY_CODE[0xc036].auth == 'PSK')
        assert (BY_CODE[0xc045].auth == 'RSA')
        assert (BY_CODE[0xc052].auth == 'RSA')
        assert (BY_CODE[0xc068].auth == 'PSK')
        assert (BY_CODE[0xc074].auth == 'ECDSA')
        assert (BY_CODE[0xc08d].auth == 'RSA')
        assert (BY_CODE[0xc09d].auth == 'RSA')
        assert (BY_CODE[0xc0a2].auth == 'RSA')
        assert (BY_CODE[0xc0ad].auth == 'ECDSA')
        assert (BY_CODE[0xcc14].auth == 'ECDSA')
        assert (BY_CODE[0xcca8].auth == 'RSA')
        assert (BY_CODE[0xccae].auth == 'PSK')

    def test_pfs(self):
        assert (BY_NAME('TLS_RSA_WITH_RC4_128_SHA').pfs == False)
        assert (BY_NAME('TLS_DHE_DSS_WITH_AES_256_CBC_SHA256').pfs == True)
        assert (BY_NAME('TLS_ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA').pfs == True)

    def test_aead(self):
        assert (BY_NAME('TLS_RSA_WITH_AES_128_CBC_SHA256').aead == False)
        assert (BY_NAME('TLS_RSA_WITH_AES_256_CCM').aead == True)
        assert (BY_NAME('TLS_DHE_RSA_WITH_AES_128_CCM_8').aead == True)
        assert (BY_NAME('TLS_DHE_PSK_WITH_AES_256_GCM_SHA384').aead == True)

    def test_anonymous(self):
        assert (BY_NAME('TLS_RSA_WITH_RC4_128_SHA').anonymous == False)
        assert (BY_NAME('TLS_DH_anon_WITH_AES_128_CBC_SHA').anonymous == True)
        assert (BY_NAME('TLS_DH_anon_EXPORT_WITH_DES40_CBC_SHA').anonymous == True)

    def test_by_name_and_code(self):
        # Special cases:
        # - explicit name
        assert (BY_CODE[0x00ff] == BY_NAME('TLS_EMPTY_RENEGOTIATION_INFO'))
        # - explicit encoding (DES_40 + CBC = DES_CBC_40)
        assert (BY_CODE[0x0026] == BY_NAME('TLS_KRB5_EXPORT_WITH_DES_CBC_40_SHA'))

        # A test from each RFC
        assert (BY_CODE[0x0005] == BY_NAME('TLS_RSA_WITH_RC4_128_SHA'))
        assert (BY_CODE[0x0021] == BY_NAME('TLS_KRB5_WITH_IDEA_CBC_SHA'))
        assert (BY_CODE[0x002d] == BY_NAME('TLS_DHE_PSK_WITH_NULL_SHA'))
        assert (BY_CODE[0x0034] == BY_NAME('TLS_DH_anon_WITH_AES_128_CBC_SHA'))
        assert (BY_CODE[0x003c] == BY_NAME('TLS_RSA_WITH_AES_128_CBC_SHA256'))
        assert (BY_CODE[0x0042] == BY_NAME('TLS_DH_DSS_WITH_CAMELLIA_128_CBC_SHA'))
        assert (BY_CODE[0x006a] == BY_NAME('TLS_DHE_DSS_WITH_AES_256_CBC_SHA256'))
        assert (BY_CODE[0x0084] == BY_NAME('TLS_RSA_WITH_CAMELLIA_256_CBC_SHA'))
        assert (BY_CODE[0x0091] == BY_NAME('TLS_DHE_PSK_WITH_AES_256_CBC_SHA'))
        assert (BY_CODE[0x0098] == BY_NAME('TLS_DH_RSA_WITH_SEED_CBC_SHA'))
        assert (BY_CODE[0x00ab] == BY_NAME('TLS_DHE_PSK_WITH_AES_256_GCM_SHA384'))
        assert (BY_CODE[0x00b0] == BY_NAME('TLS_PSK_WITH_NULL_SHA256'))
        assert (BY_CODE[0x00bb] == BY_NAME('TLS_DH_DSS_WITH_CAMELLIA_128_CBC_SHA256'))
        assert (BY_CODE[0xc008] == BY_NAME('TLS_ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA'))
        assert (BY_CODE[0xc016] == BY_NAME('TLS_ECDH_anon_WITH_RC4_128_SHA'))
        assert (BY_CODE[0xc01d] == BY_NAME('TLS_SRP_SHA_WITH_AES_128_CBC_SHA'))
        assert (BY_CODE[0xc027] == BY_NAME('TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256'))
        assert (BY_CODE[0xc036] == BY_NAME('TLS_ECDHE_PSK_WITH_AES_256_CBC_SHA'))
        assert (BY_CODE[0xc045] == BY_NAME('TLS_DHE_RSA_WITH_ARIA_256_CBC_SHA384'))
        assert (BY_CODE[0xc052] == BY_NAME('TLS_DHE_RSA_WITH_ARIA_128_GCM_SHA256'))
        assert (BY_CODE[0xc068] == BY_NAME('TLS_RSA_PSK_WITH_ARIA_128_CBC_SHA256'))
        assert (BY_CODE[0xc074] == BY_NAME('TLS_ECDH_ECDSA_WITH_CAMELLIA_128_CBC_SHA256'))
        assert (BY_CODE[0xc08d] == BY_NAME('TLS_ECDH_RSA_WITH_CAMELLIA_256_GCM_SHA384'))
        assert (BY_CODE[0xc09d] == BY_NAME('TLS_RSA_WITH_AES_256_CCM'))
        assert (BY_CODE[0xc0a2] == BY_NAME('TLS_DHE_RSA_WITH_AES_128_CCM_8'))
        assert (BY_CODE[0xc0ad] == BY_NAME('TLS_ECDHE_ECDSA_WITH_AES_256_CCM'))
        assert (BY_CODE[0xcca8] == BY_NAME('TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256'))
        assert (BY_CODE[0xccae] == BY_NAME('TLS_RSA_PSK_WITH_CHACHA20_POLY1305_SHA256'))
        assert (BY_CODE[0xcc15] == BY_NAME('OLD_TLS_DHE_RSA_WITH_CHACHA20_POLY1305_SHA256'))

