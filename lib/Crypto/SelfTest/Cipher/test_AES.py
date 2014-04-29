# -*- coding: utf-8 -*-
#
#  SelfTest/Cipher/AES.py: Self-test for the AES cipher
#
# Written in 2008 by Dwayne C. Litzenberger <dlitz@dlitz.net>
#
# ===================================================================
# The contents of this file are dedicated to the public domain.  To
# the extent that dedication to the public domain is not available,
# everyone is granted a worldwide, perpetual, royalty-free,
# non-exclusive license to exercise all rights associated with the
# contents of this file for any purpose whatsoever.
# No rights are reserved.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ===================================================================

"""Self-test suite for Crypto.Cipher.AES"""

__revision__ = "$Id$"

from Crypto.Util.py3compat import *
from binascii import hexlify

# This is a list of (plaintext, ciphertext, key[, description[, params]]) tuples.
test_data = [
    # FIPS PUB 197 test vectors
    # http://csrc.nist.gov/publications/fips/fips197/fips-197.pdf

    ('00112233445566778899aabbccddeeff', '69c4e0d86a7b0430d8cdb78070b4c55a',
        '000102030405060708090a0b0c0d0e0f', 'FIPS 197 C.1 (AES-128)'),

    ('00112233445566778899aabbccddeeff', 'dda97ca4864cdfe06eaf70a0ec0d7191',
        '000102030405060708090a0b0c0d0e0f1011121314151617',
        'FIPS 197 C.2 (AES-192)'),

    ('00112233445566778899aabbccddeeff', '8ea2b7ca516745bfeafc49904b496089',
        '000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f',
        'FIPS 197 C.3 (AES-256)'),

    # Rijndael128 test vectors
    # Downloaded 2008-09-13 from
    # http://www.iaik.tugraz.at/Research/krypto/AES/old/~rijmen/rijndael/testvalues.tar.gz

    # ecb_tbl.txt, KEYSIZE=128
    ('506812a45f08c889b97f5980038b8359', 'd8f532538289ef7d06b506a4fd5be9c9',
        '00010203050607080a0b0c0d0f101112',
        'ecb-tbl-128: I=1'),
    ('5c6d71ca30de8b8b00549984d2ec7d4b', '59ab30f4d4ee6e4ff9907ef65b1fb68c',
        '14151617191a1b1c1e1f202123242526',
        'ecb-tbl-128: I=2'),
    ('53f3f4c64f8616e4e7c56199f48f21f6', 'bf1ed2fcb2af3fd41443b56d85025cb1',
        '28292a2b2d2e2f30323334353738393a',
        'ecb-tbl-128: I=3'),
    ('a1eb65a3487165fb0f1c27ff9959f703', '7316632d5c32233edcb0780560eae8b2',
        '3c3d3e3f41424344464748494b4c4d4e',
        'ecb-tbl-128: I=4'),
    ('3553ecf0b1739558b08e350a98a39bfa', '408c073e3e2538072b72625e68b8364b',
        '50515253555657585a5b5c5d5f606162',
        'ecb-tbl-128: I=5'),
    ('67429969490b9711ae2b01dc497afde8', 'e1f94dfa776597beaca262f2f6366fea',
        '64656667696a6b6c6e6f707173747576',
        'ecb-tbl-128: I=6'),
    ('93385c1f2aec8bed192f5a8e161dd508', 'f29e986c6a1c27d7b29ffd7ee92b75f1',
        '78797a7b7d7e7f80828384858788898a',
        'ecb-tbl-128: I=7'),
    ('b5bf946be19beb8db3983b5f4c6e8ddb', '131c886a57f8c2e713aba6955e2b55b5',
        '8c8d8e8f91929394969798999b9c9d9e',
        'ecb-tbl-128: I=8'),
    ('41321ee10e21bd907227c4450ff42324', 'd2ab7662df9b8c740210e5eeb61c199d',
        'a0a1a2a3a5a6a7a8aaabacadafb0b1b2',
        'ecb-tbl-128: I=9'),
    ('00a82f59c91c8486d12c0a80124f6089', '14c10554b2859c484cab5869bbe7c470',
        'b4b5b6b7b9babbbcbebfc0c1c3c4c5c6',
        'ecb-tbl-128: I=10'),
    ('7ce0fd076754691b4bbd9faf8a1372fe', 'db4d498f0a49cf55445d502c1f9ab3b5',
        'c8c9cacbcdcecfd0d2d3d4d5d7d8d9da',
        'ecb-tbl-128: I=11'),
    ('23605a8243d07764541bc5ad355b3129', '6d96fef7d66590a77a77bb2056667f7f',
        'dcdddedfe1e2e3e4e6e7e8e9ebecedee',
        'ecb-tbl-128: I=12'),
    ('12a8cfa23ea764fd876232b4e842bc44', '316fb68edba736c53e78477bf913725c',
        'f0f1f2f3f5f6f7f8fafbfcfdfe010002',
        'ecb-tbl-128: I=13'),
    ('bcaf32415e8308b3723e5fdd853ccc80', '6936f2b93af8397fd3a771fc011c8c37',
        '04050607090a0b0c0e0f101113141516',
        'ecb-tbl-128: I=14'),
    ('89afae685d801ad747ace91fc49adde0', 'f3f92f7a9c59179c1fcc2c2ba0b082cd',
        '2c2d2e2f31323334363738393b3c3d3e',
        'ecb-tbl-128: I=15'),
    ('f521d07b484357c4a69e76124a634216', '6a95ea659ee3889158e7a9152ff04ebc',
        '40414243454647484a4b4c4d4f505152',
        'ecb-tbl-128: I=16'),
    ('3e23b3bc065bcc152407e23896d77783', '1959338344e945670678a5d432c90b93',
        '54555657595a5b5c5e5f606163646566',
        'ecb-tbl-128: I=17'),
    ('79f0fba002be1744670e7e99290d8f52', 'e49bddd2369b83ee66e6c75a1161b394',
        '68696a6b6d6e6f70727374757778797a',
        'ecb-tbl-128: I=18'),
    ('da23fe9d5bd63e1d72e3dafbe21a6c2a', 'd3388f19057ff704b70784164a74867d',
        '7c7d7e7f81828384868788898b8c8d8e',
        'ecb-tbl-128: I=19'),
    ('e3f5698ba90b6a022efd7db2c7e6c823', '23aa03e2d5e4cd24f3217e596480d1e1',
        'a4a5a6a7a9aaabacaeafb0b1b3b4b5b6',
        'ecb-tbl-128: I=20'),
    ('bdc2691d4f1b73d2700679c3bcbf9c6e', 'c84113d68b666ab2a50a8bdb222e91b9',
        'e0e1e2e3e5e6e7e8eaebecedeff0f1f2',
        'ecb-tbl-128: I=21'),
    ('ba74e02093217ee1ba1b42bd5624349a', 'ac02403981cd4340b507963db65cb7b6',
        '08090a0b0d0e0f10121314151718191a',
        'ecb-tbl-128: I=22'),
    ('b5c593b5851c57fbf8b3f57715e8f680', '8d1299236223359474011f6bf5088414',
        '6c6d6e6f71727374767778797b7c7d7e',
        'ecb-tbl-128: I=23'),
    ('3da9bd9cec072381788f9387c3bbf4ee', '5a1d6ab8605505f7977e55b9a54d9b90',
        '80818283858687888a8b8c8d8f909192',
        'ecb-tbl-128: I=24'),
    ('4197f3051121702ab65d316b3c637374', '72e9c2d519cf555e4208805aabe3b258',
        '94959697999a9b9c9e9fa0a1a3a4a5a6',
        'ecb-tbl-128: I=25'),
    ('9f46c62ec4f6ee3f6e8c62554bc48ab7', 'a8f3e81c4a23a39ef4d745dffe026e80',
        'a8a9aaabadaeafb0b2b3b4b5b7b8b9ba',
        'ecb-tbl-128: I=26'),
    ('0220673fe9e699a4ebc8e0dbeb6979c8', '546f646449d31458f9eb4ef5483aee6c',
        'bcbdbebfc1c2c3c4c6c7c8c9cbcccdce',
        'ecb-tbl-128: I=27'),
    ('b2b99171337ded9bc8c2c23ff6f18867', '4dbe4bc84ac797c0ee4efb7f1a07401c',
        'd0d1d2d3d5d6d7d8dadbdcdddfe0e1e2',
        'ecb-tbl-128: I=28'),
    ('a7facf4e301e984e5efeefd645b23505', '25e10bfb411bbd4d625ac8795c8ca3b3',
        'e4e5e6e7e9eaebeceeeff0f1f3f4f5f6',
        'ecb-tbl-128: I=29'),
    ('f7c762e4a9819160fd7acfb6c4eedcdd', '315637405054ec803614e43def177579',
        'f8f9fafbfdfefe00020304050708090a',
        'ecb-tbl-128: I=30'),
    ('9b64fc21ea08709f4915436faa70f1be', '60c5bc8a1410247295c6386c59e572a8',
        '0c0d0e0f11121314161718191b1c1d1e',
        'ecb-tbl-128: I=31'),
    ('52af2c3de07ee6777f55a4abfc100b3f', '01366fc8ca52dfe055d6a00a76471ba6',
        '20212223252627282a2b2c2d2f303132',
        'ecb-tbl-128: I=32'),
    ('2fca001224386c57aa3f968cbe2c816f', 'ecc46595516ec612449c3f581e7d42ff',
        '34353637393a3b3c3e3f404143444546',
        'ecb-tbl-128: I=33'),
    ('4149c73658a4a9c564342755ee2c132f', '6b7ffe4c602a154b06ee9c7dab5331c9',
        '48494a4b4d4e4f50525354555758595a',
        'ecb-tbl-128: I=34'),
    ('af60005a00a1772f7c07a48a923c23d2', '7da234c14039a240dd02dd0fbf84eb67',
        '5c5d5e5f61626364666768696b6c6d6e',
        'ecb-tbl-128: I=35'),
    ('6fccbc28363759914b6f0280afaf20c6', 'c7dc217d9e3604ffe7e91f080ecd5a3a',
        '70717273757677787a7b7c7d7f808182',
        'ecb-tbl-128: I=36'),
    ('7d82a43ddf4fefa2fc5947499884d386', '37785901863f5c81260ea41e7580cda5',
        '84858687898a8b8c8e8f909193949596',
        'ecb-tbl-128: I=37'),
    ('5d5a990eaab9093afe4ce254dfa49ef9', 'a07b9338e92ed105e6ad720fccce9fe4',
        '98999a9b9d9e9fa0a2a3a4a5a7a8a9aa',
        'ecb-tbl-128: I=38'),
    ('4cd1e2fd3f4434b553aae453f0ed1a02', 'ae0fb9722418cc21a7da816bbc61322c',
        'acadaeafb1b2b3b4b6b7b8b9bbbcbdbe',
        'ecb-tbl-128: I=39'),
    ('5a2c9a9641d4299125fa1b9363104b5e', 'c826a193080ff91ffb21f71d3373c877',
        'c0c1c2c3c5c6c7c8cacbcccdcfd0d1d2',
        'ecb-tbl-128: I=40'),
    ('b517fe34c0fa217d341740bfd4fe8dd4', '1181b11b0e494e8d8b0aa6b1d5ac2c48',
        'd4d5d6d7d9dadbdcdedfe0e1e3e4e5e6',
        'ecb-tbl-128: I=41'),
    ('014baf2278a69d331d5180103643e99a', '6743c3d1519ab4f2cd9a78ab09a511bd',
        'e8e9eaebedeeeff0f2f3f4f5f7f8f9fa',
        'ecb-tbl-128: I=42'),
    ('b529bd8164f20d0aa443d4932116841c', 'dc55c076d52bacdf2eefd952946a439d',
        'fcfdfeff01020304060708090b0c0d0e',
        'ecb-tbl-128: I=43'),
    ('2e596dcbb2f33d4216a1176d5bd1e456', '711b17b590ffc72b5c8e342b601e8003',
        '10111213151617181a1b1c1d1f202122',
        'ecb-tbl-128: I=44'),
    ('7274a1ea2b7ee2424e9a0e4673689143', '19983bb0950783a537e1339f4aa21c75',
        '24252627292a2b2c2e2f303133343536',
        'ecb-tbl-128: I=45'),
    ('ae20020bd4f13e9d90140bee3b5d26af', '3ba7762e15554169c0f4fa39164c410c',
        '38393a3b3d3e3f40424344454748494a',
        'ecb-tbl-128: I=46'),
    ('baac065da7ac26e855e79c8849d75a02', 'a0564c41245afca7af8aa2e0e588ea89',
        '4c4d4e4f51525354565758595b5c5d5e',
        'ecb-tbl-128: I=47'),
    ('7c917d8d1d45fab9e2540e28832540cc', '5e36a42a2e099f54ae85ecd92e2381ed',
        '60616263656667686a6b6c6d6f707172',
        'ecb-tbl-128: I=48'),
    ('bde6f89e16daadb0e847a2a614566a91', '770036f878cd0f6ca2268172f106f2fe',
        '74757677797a7b7c7e7f808183848586',
        'ecb-tbl-128: I=49'),
    ('c9de163725f1f5be44ebb1db51d07fbc', '7e4e03908b716116443ccf7c94e7c259',
        '88898a8b8d8e8f90929394959798999a',
        'ecb-tbl-128: I=50'),
    ('3af57a58f0c07dffa669572b521e2b92', '482735a48c30613a242dd494c7f9185d',
        '9c9d9e9fa1a2a3a4a6a7a8a9abacadae',
        'ecb-tbl-128: I=51'),
    ('3d5ebac306dde4604f1b4fbbbfcdae55', 'b4c0f6c9d4d7079addf9369fc081061d',
        'b0b1b2b3b5b6b7b8babbbcbdbfc0c1c2',
        'ecb-tbl-128: I=52'),
    ('c2dfa91bceb76a1183c995020ac0b556', 'd5810fe0509ac53edcd74f89962e6270',
        'c4c5c6c7c9cacbcccecfd0d1d3d4d5d6',
        'ecb-tbl-128: I=53'),
    ('c70f54305885e9a0746d01ec56c8596b', '03f17a16b3f91848269ecdd38ebb2165',
        'd8d9dadbdddedfe0e2e3e4e5e7e8e9ea',
        'ecb-tbl-128: I=54'),
    ('c4f81b610e98012ce000182050c0c2b2', 'da1248c3180348bad4a93b4d9856c9df',
        'ecedeeeff1f2f3f4f6f7f8f9fbfcfdfe',
        'ecb-tbl-128: I=55'),
    ('eaab86b1d02a95d7404eff67489f97d4', '3d10d7b63f3452c06cdf6cce18be0c2c',
        '00010203050607080a0b0c0d0f101112',
        'ecb-tbl-128: I=56'),
    ('7c55bdb40b88870b52bec3738de82886', '4ab823e7477dfddc0e6789018fcb6258',
        '14151617191a1b1c1e1f202123242526',
        'ecb-tbl-128: I=57'),
    ('ba6eaa88371ff0a3bd875e3f2a975ce0', 'e6478ba56a77e70cfdaa5c843abde30e',
        '28292a2b2d2e2f30323334353738393a',
        'ecb-tbl-128: I=58'),
    ('08059130c4c24bd30cf0575e4e0373dc', '1673064895fbeaf7f09c5429ff75772d',
        '3c3d3e3f41424344464748494b4c4d4e',
        'ecb-tbl-128: I=59'),
    ('9a8eab004ef53093dfcf96f57e7eda82', '4488033ae9f2efd0ca9383bfca1a94e9',
        '50515253555657585a5b5c5d5f606162',
        'ecb-tbl-128: I=60'),
    ('0745b589e2400c25f117b1d796c28129', '978f3b8c8f9d6f46626cac3c0bcb9217',
        '64656667696a6b6c6e6f707173747576',
        'ecb-tbl-128: I=61'),
    ('2f1777781216cec3f044f134b1b92bbe', 'e08c8a7e582e15e5527f1d9e2eecb236',
        '78797a7b7d7e7f80828384858788898a',
        'ecb-tbl-128: I=62'),
    ('353a779ffc541b3a3805d90ce17580fc', 'cec155b76ac5ffda4cf4f9ca91e49a7a',
        '8c8d8e8f91929394969798999b9c9d9e',
        'ecb-tbl-128: I=63'),
    ('1a1eae4415cefcf08c4ac1c8f68bea8f', 'd5ac7165763225dd2a38cdc6862c29ad',
        'a0a1a2a3a5a6a7a8aaabacadafb0b1b2',
        'ecb-tbl-128: I=64'),
    ('e6e7e4e5b0b3b2b5d4d5aaab16111013', '03680fe19f7ce7275452020be70e8204',
        'b4b5b6b7b9babbbcbebfc0c1c3c4c5c6',
        'ecb-tbl-128: I=65'),
    ('f8f9fafbfbf8f9e677767170efe0e1e2', '461df740c9781c388e94bb861ceb54f6',
        'c8c9cacbcdcecfd0d2d3d4d5d7d8d9da',
        'ecb-tbl-128: I=66'),
    ('63626160a1a2a3a445444b4a75727370', '451bd60367f96483042742219786a074',
        'dcdddedfe1e2e3e4e6e7e8e9ebecedee',
        'ecb-tbl-128: I=67'),
    ('717073720605040b2d2c2b2a05fafbf9', 'e4dfa42671a02e57ef173b85c0ea9f2b',
        'f0f1f2f3f5f6f7f8fafbfcfdfe010002',
        'ecb-tbl-128: I=68'),
    ('78797a7beae9e8ef3736292891969794', 'ed11b89e76274282227d854700a78b9e',
        '04050607090a0b0c0e0f101113141516',
        'ecb-tbl-128: I=69'),
    ('838281803231300fdddcdbdaa0afaead', '433946eaa51ea47af33895f2b90b3b75',
        '18191a1b1d1e1f20222324252728292a',
        'ecb-tbl-128: I=70'),
    ('18191a1bbfbcbdba75747b7a7f78797a', '6bc6d616a5d7d0284a5910ab35022528',
        '2c2d2e2f31323334363738393b3c3d3e',
        'ecb-tbl-128: I=71'),
    ('848586879b989996a3a2a5a4849b9a99', 'd2a920ecfe919d354b5f49eae9719c98',
        '40414243454647484a4b4c4d4f505152',
        'ecb-tbl-128: I=72'),
    ('0001020322212027cacbf4f551565754', '3a061b17f6a92885efbd0676985b373d',
        '54555657595a5b5c5e5f606163646566',
        'ecb-tbl-128: I=73'),
    ('cecfcccdafacadb2515057564a454447', 'fadeec16e33ea2f4688499d157e20d8f',
        '68696a6b6d6e6f70727374757778797a',
        'ecb-tbl-128: I=74'),
    ('92939091cdcecfc813121d1c80878685', '5cdefede59601aa3c3cda36fa6b1fa13',
        '7c7d7e7f81828384868788898b8c8d8e',
        'ecb-tbl-128: I=75'),
    ('d2d3d0d16f6c6d6259585f5ed1eeefec', '9574b00039844d92ebba7ee8719265f8',
        '90919293959697989a9b9c9d9fa0a1a2',
        'ecb-tbl-128: I=76'),
    ('acadaeaf878485820f0e1110d5d2d3d0', '9a9cf33758671787e5006928188643fa',
        'a4a5a6a7a9aaabacaeafb0b1b3b4b5b6',
        'ecb-tbl-128: I=77'),
    ('9091929364676619e6e7e0e1757a7b78', '2cddd634c846ba66bb46cbfea4a674f9',
        'b8b9babbbdbebfc0c2c3c4c5c7c8c9ca',
        'ecb-tbl-128: I=78'),
    ('babbb8b98a89888f74757a7b92959497', 'd28bae029393c3e7e26e9fafbbb4b98f',
        'cccdcecfd1d2d3d4d6d7d8d9dbdcddde',
        'ecb-tbl-128: I=79'),
    ('8d8c8f8e6e6d6c633b3a3d3ccad5d4d7', 'ec27529b1bee0a9ab6a0d73ebc82e9b7',
        'e0e1e2e3e5e6e7e8eaebecedeff0f1f2',
        'ecb-tbl-128: I=80'),
    ('86878485010203040808f7f767606162', '3cb25c09472aff6ee7e2b47ccd7ccb17',
        'f4f5f6f7f9fafbfcfefe010103040506',
        'ecb-tbl-128: I=81'),
    ('8e8f8c8d656667788a8b8c8d010e0f0c', 'dee33103a7283370d725e44ca38f8fe5',
        '08090a0b0d0e0f10121314151718191a',
        'ecb-tbl-128: I=82'),
    ('c8c9cacb858687807a7b7475e7e0e1e2', '27f9bcd1aac64bffc11e7815702c1a69',
        '1c1d1e1f21222324262728292b2c2d2e',
        'ecb-tbl-128: I=83'),
    ('6d6c6f6e5053525d8c8d8a8badd2d3d0', '5df534ffad4ed0749a9988e9849d0021',
        '30313233353637383a3b3c3d3f404142',
        'ecb-tbl-128: I=84'),
    ('28292a2b393a3b3c0607181903040506', 'a48bee75db04fb60ca2b80f752a8421b',
        '44454647494a4b4c4e4f505153545556',
        'ecb-tbl-128: I=85'),
    ('a5a4a7a6b0b3b28ddbdadddcbdb2b3b0', '024c8cf70bc86ee5ce03678cb7af45f9',
        '58595a5b5d5e5f60626364656768696a',
        'ecb-tbl-128: I=86'),
    ('323330316467666130313e3f2c2b2a29', '3c19ac0f8a3a3862ce577831301e166b',
        '6c6d6e6f71727374767778797b7c7d7e',
        'ecb-tbl-128: I=87'),
    ('27262524080b0a05171611100b141516', 'c5e355b796a57421d59ca6be82e73bca',
        '80818283858687888a8b8c8d8f909192',
        'ecb-tbl-128: I=88'),
    ('040506074142434435340b0aa3a4a5a6', 'd94033276417abfb05a69d15b6e386e2',
        '94959697999a9b9c9e9fa0a1a3a4a5a6',
        'ecb-tbl-128: I=89'),
    ('242526271112130c61606766bdb2b3b0', '24b36559ea3a9b9b958fe6da3e5b8d85',
        'a8a9aaabadaeafb0b2b3b4b5b7b8b9ba',
        'ecb-tbl-128: I=90'),
    ('4b4a4948252627209e9f9091cec9c8cb', '20fd4feaa0e8bf0cce7861d74ef4cb72',
        'bcbdbebfc1c2c3c4c6c7c8c9cbcccdce',
        'ecb-tbl-128: I=91'),
    ('68696a6b6665646b9f9e9998d9e6e7e4', '350e20d5174277b9ec314c501570a11d',
        'd0d1d2d3d5d6d7d8dadbdcdddfe0e1e2',
        'ecb-tbl-128: I=92'),
    ('34353637c5c6c7c0f0f1eeef7c7b7a79', '87a29d61b7c604d238fe73045a7efd57',
        'e4e5e6e7e9eaebeceeeff0f1f3f4f5f6',
        'ecb-tbl-128: I=93'),
    ('32333031c2c1c13f0d0c0b0a050a0b08', '2c3164c1cc7d0064816bdc0faa362c52',
        'f8f9fafbfdfefe00020304050708090a',
        'ecb-tbl-128: I=94'),
    ('cdcccfcebebdbcbbabaaa5a4181f1e1d', '195fe5e8a05a2ed594f6e4400eee10b3',
        '0c0d0e0f11121314161718191b1c1d1e',
        'ecb-tbl-128: I=95'),
    ('212023223635343ba0a1a6a7445b5a59', 'e4663df19b9a21a5a284c2bd7f905025',
        '20212223252627282a2b2c2d2f303132',
        'ecb-tbl-128: I=96'),
    ('0e0f0c0da8abaaad2f2e515002050407', '21b88714cfb4e2a933bd281a2c4743fd',
        '34353637393a3b3c3e3f404143444546',
        'ecb-tbl-128: I=97'),
    ('070605042a2928378e8f8889bdb2b3b0', 'cbfc3980d704fd0fc54378ab84e17870',
        '48494a4b4d4e4f50525354555758595a',
        'ecb-tbl-128: I=98'),
    ('cbcac9c893909196a9a8a7a6a5a2a3a0', 'bc5144baa48bdeb8b63e22e03da418ef',
        '5c5d5e5f61626364666768696b6c6d6e',
        'ecb-tbl-128: I=99'),
    ('80818283c1c2c3cc9c9d9a9b0cf3f2f1', '5a1dbaef1ee2984b8395da3bdffa3ccc',
        '70717273757677787a7b7c7d7f808182',
        'ecb-tbl-128: I=100'),
    ('1213101125262720fafbe4e5b1b6b7b4', 'f0b11cd0729dfcc80cec903d97159574',
        '84858687898a8b8c8e8f909193949596',
        'ecb-tbl-128: I=101'),
    ('7f7e7d7c3033320d97969190222d2c2f', '9f95314acfddc6d1914b7f19a9cc8209',
        '98999a9b9d9e9fa0a2a3a4a5a7a8a9aa',
        'ecb-tbl-128: I=102'),
    ('4e4f4c4d484b4a4d81808f8e53545556', '595736f6f0f70914a94e9e007f022519',
        'acadaeafb1b2b3b4b6b7b8b9bbbcbdbe',
        'ecb-tbl-128: I=103'),
    ('dcdddedfb0b3b2bd15141312a1bebfbc', '1f19f57892cae586fcdfb4c694deb183',
        'c0c1c2c3c5c6c7c8cacbcccdcfd0d1d2',
        'ecb-tbl-128: I=104'),
    ('93929190282b2a2dc4c5fafb92959497', '540700ee1f6f3dab0b3eddf6caee1ef5',
        'd4d5d6d7d9dadbdcdedfe0e1e3e4e5e6',
        'ecb-tbl-128: I=105'),
    ('f5f4f7f6c4c7c6d9373631307e717073', '14a342a91019a331687a2254e6626ca2',
        'e8e9eaebedeeeff0f2f3f4f5f7f8f9fa',
        'ecb-tbl-128: I=106'),
    ('93929190b6b5b4b364656a6b05020300', '7b25f3c3b2eea18d743ef283140f29ff',
        'fcfdfeff01020304060708090b0c0d0e',
        'ecb-tbl-128: I=107'),
    ('babbb8b90d0e0f00a4a5a2a3043b3a39', '46c2587d66e5e6fa7f7ca6411ad28047',
        '10111213151617181a1b1c1d1f202122',
        'ecb-tbl-128: I=108'),
    ('d8d9dadb7f7c7d7a10110e0f787f7e7d', '09470e72229d954ed5ee73886dfeeba9',
        '24252627292a2b2c2e2f303133343536',
        'ecb-tbl-128: I=109'),
    ('fefffcfdefeced923b3a3d3c6768696a', 'd77c03de92d4d0d79ef8d4824ef365eb',
        '38393a3b3d3e3f40424344454748494a',
        'ecb-tbl-128: I=110'),
    ('d6d7d4d58a89888f96979899a5a2a3a0', '1d190219f290e0f1715d152d41a23593',
        '4c4d4e4f51525354565758595b5c5d5e',
        'ecb-tbl-128: I=111'),
    ('18191a1ba8abaaa5303136379b848586', 'a2cd332ce3a0818769616292e87f757b',
        '60616263656667686a6b6c6d6f707172',
        'ecb-tbl-128: I=112'),
    ('6b6a6968a4a7a6a1d6d72829b0b7b6b5', 'd54afa6ce60fbf9341a3690e21385102',
        '74757677797a7b7c7e7f808183848586',
        'ecb-tbl-128: I=113'),
    ('000102038a89889755545352a6a9a8ab', '06e5c364ded628a3f5e05e613e356f46',
        '88898a8b8d8e8f90929394959798999a',
        'ecb-tbl-128: I=114'),
    ('2d2c2f2eb3b0b1b6b6b7b8b9f2f5f4f7', 'eae63c0e62556dac85d221099896355a',
        '9c9d9e9fa1a2a3a4a6a7a8a9abacadae',
        'ecb-tbl-128: I=115'),
    ('979695943536373856575051e09f9e9d', '1fed060e2c6fc93ee764403a889985a2',
        'b0b1b2b3b5b6b7b8babbbcbdbfc0c1c2',
        'ecb-tbl-128: I=116'),
    ('a4a5a6a7989b9a9db1b0afae7a7d7c7f', 'c25235c1a30fdec1c7cb5c5737b2a588',
        'c4c5c6c7c9cacbcccecfd0d1d3d4d5d6',
        'ecb-tbl-128: I=117'),
    ('c1c0c3c2686b6a55a8a9aeafeae5e4e7', '796dbef95147d4d30873ad8b7b92efc0',
        'd8d9dadbdddedfe0e2e3e4e5e7e8e9ea',
        'ecb-tbl-128: I=118'),
    ('c1c0c3c2141716118c8d828364636261', 'cbcf0fb34d98d0bd5c22ce37211a46bf',
        'ecedeeeff1f2f3f4f6f7f8f9fbfcfdfe',
        'ecb-tbl-128: I=119'),
    ('93929190cccfcec196979091e0fffefd', '94b44da6466126cafa7c7fd09063fc24',
        '00010203050607080a0b0c0d0f101112',
        'ecb-tbl-128: I=120'),
    ('b4b5b6b7f9fafbfc25241b1a6e69686b', 'd78c5b5ebf9b4dbda6ae506c5074c8fe',
        '14151617191a1b1c1e1f202123242526',
        'ecb-tbl-128: I=121'),
    ('868784850704051ac7c6c1c08788898a', '6c27444c27204b043812cf8cf95f9769',
        '28292a2b2d2e2f30323334353738393a',
        'ecb-tbl-128: I=122'),
    ('f4f5f6f7aaa9a8affdfcf3f277707172', 'be94524ee5a2aa50bba8b75f4c0aebcf',
        '3c3d3e3f41424344464748494b4c4d4e',
        'ecb-tbl-128: I=123'),
    ('d3d2d1d00605040bc3c2c5c43e010003', 'a0aeaae91ba9f31f51aeb3588cf3a39e',
        '50515253555657585a5b5c5d5f606162',
        'ecb-tbl-128: I=124'),
    ('73727170424140476a6b74750d0a0b08', '275297779c28266ef9fe4c6a13c08488',
        '64656667696a6b6c6e6f707173747576',
        'ecb-tbl-128: I=125'),
    ('c2c3c0c10a0908f754555253a1aeafac', '86523d92bb8672cb01cf4a77fd725882',
        '78797a7b7d7e7f80828384858788898a',
        'ecb-tbl-128: I=126'),
    ('6d6c6f6ef8fbfafd82838c8df8fffefd', '4b8327640e9f33322a04dd96fcbf9a36',
        '8c8d8e8f91929394969798999b9c9d9e',
        'ecb-tbl-128: I=127'),
    ('f5f4f7f684878689a6a7a0a1d2cdcccf', 'ce52af650d088ca559425223f4d32694',
        'a0a1a2a3a5a6a7a8aaabacadafb0b1b2',
        'ecb-tbl-128: I=128'),

    # ecb_tbl.txt, KEYSIZE=192
    ('2d33eef2c0430a8a9ebf45e809c40bb6', 'dff4945e0336df4c1c56bc700eff837f',
        '00010203050607080a0b0c0d0f10111214151617191a1b1c',
        'ecb-tbl-192: I=1'),
    ('6aa375d1fa155a61fb72353e0a5a8756', 'b6fddef4752765e347d5d2dc196d1252',
        '1e1f20212324252628292a2b2d2e2f30323334353738393a',
        'ecb-tbl-192: I=2'),
    ('bc3736518b9490dcb8ed60eb26758ed4', 'd23684e3d963b3afcf1a114aca90cbd6',
        '3c3d3e3f41424344464748494b4c4d4e5051525355565758',
        'ecb-tbl-192: I=3'),
    ('aa214402b46cffb9f761ec11263a311e', '3a7ac027753e2a18c2ceab9e17c11fd0',
        '5a5b5c5d5f60616264656667696a6b6c6e6f707173747576',
        'ecb-tbl-192: I=4'),
    ('02aea86e572eeab66b2c3af5e9a46fd6', '8f6786bd007528ba26603c1601cdd0d8',
        '78797a7b7d7e7f80828384858788898a8c8d8e8f91929394',
        'ecb-tbl-192: I=5'),
    ('e2aef6acc33b965c4fa1f91c75ff6f36', 'd17d073b01e71502e28b47ab551168b3',
        '969798999b9c9d9ea0a1a2a3a5a6a7a8aaabacadafb0b1b2',
        'ecb-tbl-192: I=6'),
    ('0659df46427162b9434865dd9499f91d', 'a469da517119fab95876f41d06d40ffa',
        'b4b5b6b7b9babbbcbebfc0c1c3c4c5c6c8c9cacbcdcecfd0',
        'ecb-tbl-192: I=7'),
    ('49a44239c748feb456f59c276a5658df', '6091aa3b695c11f5c0b6ad26d3d862ff',
        'd2d3d4d5d7d8d9dadcdddedfe1e2e3e4e6e7e8e9ebecedee',
        'ecb-tbl-192: I=8'),
    ('66208f6e9d04525bdedb2733b6a6be37', '70f9e67f9f8df1294131662dc6e69364',
        'f0f1f2f3f5f6f7f8fafbfcfdfe01000204050607090a0b0c',
        'ecb-tbl-192: I=9'),
    ('3393f8dfc729c97f5480b950bc9666b0', 'd154dcafad8b207fa5cbc95e9996b559',
        '0e0f10111314151618191a1b1d1e1f20222324252728292a',
        'ecb-tbl-192: I=10'),
    ('606834c8ce063f3234cf1145325dbd71', '4934d541e8b46fa339c805a7aeb9e5da',
        '2c2d2e2f31323334363738393b3c3d3e4041424345464748',
        'ecb-tbl-192: I=11'),
    ('fec1c04f529bbd17d8cecfcc4718b17f', '62564c738f3efe186e1a127a0c4d3c61',
        '4a4b4c4d4f50515254555657595a5b5c5e5f606163646566',
        'ecb-tbl-192: I=12'),
    ('32df99b431ed5dc5acf8caf6dc6ce475', '07805aa043986eb23693e23bef8f3438',
        '68696a6b6d6e6f70727374757778797a7c7d7e7f81828384',
        'ecb-tbl-192: I=13'),
    ('7fdc2b746f3f665296943b83710d1f82', 'df0b4931038bade848dee3b4b85aa44b',
        '868788898b8c8d8e90919293959697989a9b9c9d9fa0a1a2',
        'ecb-tbl-192: I=14'),
    ('8fba1510a3c5b87e2eaa3f7a91455ca2', '592d5fded76582e4143c65099309477c',
        'a4a5a6a7a9aaabacaeafb0b1b3b4b5b6b8b9babbbdbebfc0',
        'ecb-tbl-192: I=15'),
    ('2c9b468b1c2eed92578d41b0716b223b', 'c9b8d6545580d3dfbcdd09b954ed4e92',
        'c2c3c4c5c7c8c9cacccdcecfd1d2d3d4d6d7d8d9dbdcddde',
        'ecb-tbl-192: I=16'),
    ('0a2bbf0efc6bc0034f8a03433fca1b1a', '5dccd5d6eb7c1b42acb008201df707a0',
        'e0e1e2e3e5e6e7e8eaebecedeff0f1f2f4f5f6f7f9fafbfc',
        'ecb-tbl-192: I=17'),
    ('25260e1f31f4104d387222e70632504b', 'a2a91682ffeb6ed1d34340946829e6f9',
        'fefe01010304050608090a0b0d0e0f10121314151718191a',
        'ecb-tbl-192: I=18'),
    ('c527d25a49f08a5228d338642ae65137', 'e45d185b797000348d9267960a68435d',
        '1c1d1e1f21222324262728292b2c2d2e3031323335363738',
        'ecb-tbl-192: I=19'),
    ('3b49fc081432f5890d0e3d87e884a69e', '45e060dae5901cda8089e10d4f4c246b',
        '3a3b3c3d3f40414244454647494a4b4c4e4f505153545556',
        'ecb-tbl-192: I=20'),
    ('d173f9ed1e57597e166931df2754a083', 'f6951afacc0079a369c71fdcff45df50',
        '58595a5b5d5e5f60626364656768696a6c6d6e6f71727374',
        'ecb-tbl-192: I=21'),
    ('8c2b7cafa5afe7f13562daeae1adede0', '9e95e00f351d5b3ac3d0e22e626ddad6',
        '767778797b7c7d7e80818283858687888a8b8c8d8f909192',
        'ecb-tbl-192: I=22'),
    ('aaf4ec8c1a815aeb826cab741339532c', '9cb566ff26d92dad083b51fdc18c173c',
        '94959697999a9b9c9e9fa0a1a3a4a5a6a8a9aaabadaeafb0',
        'ecb-tbl-192: I=23'),
    ('40be8c5d9108e663f38f1a2395279ecf', 'c9c82766176a9b228eb9a974a010b4fb',
        'd0d1d2d3d5d6d7d8dadbdcdddfe0e1e2e4e5e6e7e9eaebec',
        'ecb-tbl-192: I=24'),
    ('0c8ad9bc32d43e04716753aa4cfbe351', 'd8e26aa02945881d5137f1c1e1386e88',
        '2a2b2c2d2f30313234353637393a3b3c3e3f404143444546',
        'ecb-tbl-192: I=25'),
    ('1407b1d5f87d63357c8dc7ebbaebbfee', 'c0e024ccd68ff5ffa4d139c355a77c55',
        '48494a4b4d4e4f50525354555758595a5c5d5e5f61626364',
        'ecb-tbl-192: I=26'),
    ('e62734d1ae3378c4549e939e6f123416', '0b18b3d16f491619da338640df391d43',
        '84858687898a8b8c8e8f90919394959698999a9b9d9e9fa0',
        'ecb-tbl-192: I=27'),
    ('5a752cff2a176db1a1de77f2d2cdee41', 'dbe09ac8f66027bf20cb6e434f252efc',
        'a2a3a4a5a7a8a9aaacadaeafb1b2b3b4b6b7b8b9bbbcbdbe',
        'ecb-tbl-192: I=28'),
    ('a9c8c3a4eabedc80c64730ddd018cd88', '6d04e5e43c5b9cbe05feb9606b6480fe',
        'c0c1c2c3c5c6c7c8cacbcccdcfd0d1d2d4d5d6d7d9dadbdc',
        'ecb-tbl-192: I=29'),
    ('ee9b3dbbdb86180072130834d305999a', 'dd1d6553b96be526d9fee0fbd7176866',
        '1a1b1c1d1f20212224252627292a2b2c2e2f303133343536',
        'ecb-tbl-192: I=30'),
    ('a7fa8c3586b8ebde7568ead6f634a879', '0260ca7e3f979fd015b0dd4690e16d2a',
        '38393a3b3d3e3f40424344454748494a4c4d4e4f51525354',
        'ecb-tbl-192: I=31'),
    ('37e0f4a87f127d45ac936fe7ad88c10a', '9893734de10edcc8a67c3b110b8b8cc6',
        '929394959798999a9c9d9e9fa1a2a3a4a6a7a8a9abacadae',
        'ecb-tbl-192: I=32'),
    ('3f77d8b5d92bac148e4e46f697a535c5', '93b30b750516b2d18808d710c2ee84ef',
        '464748494b4c4d4e50515253555657585a5b5c5d5f606162',
        'ecb-tbl-192: I=33'),
    ('d25ebb686c40f7e2c4da1014936571ca', '16f65fa47be3cb5e6dfe7c6c37016c0e',
        '828384858788898a8c8d8e8f91929394969798999b9c9d9e',
        'ecb-tbl-192: I=34'),
    ('4f1c769d1e5b0552c7eca84dea26a549', 'f3847210d5391e2360608e5acb560581',
        'a0a1a2a3a5a6a7a8aaabacadafb0b1b2b4b5b6b7b9babbbc',
        'ecb-tbl-192: I=35'),
    ('8548e2f882d7584d0fafc54372b6633a', '8754462cd223366d0753913e6af2643d',
        'bebfc0c1c3c4c5c6c8c9cacbcdcecfd0d2d3d4d5d7d8d9da',
        'ecb-tbl-192: I=36'),
    ('87d7a336cb476f177cd2a51af2a62cdf', '1ea20617468d1b806a1fd58145462017',
        'dcdddedfe1e2e3e4e6e7e8e9ebecedeef0f1f2f3f5f6f7f8',
        'ecb-tbl-192: I=37'),
    ('03b1feac668c4e485c1065dfc22b44ee', '3b155d927355d737c6be9dda60136e2e',
        'fafbfcfdfe01000204050607090a0b0c0e0f101113141516',
        'ecb-tbl-192: I=38'),
    ('bda15e66819fa72d653a6866aa287962', '26144f7b66daa91b6333dbd3850502b3',
        '18191a1b1d1e1f20222324252728292a2c2d2e2f31323334',
        'ecb-tbl-192: I=39'),
    ('4d0c7a0d2505b80bf8b62ceb12467f0a', 'e4f9a4ab52ced8134c649bf319ebcc90',
        '363738393b3c3d3e40414243454647484a4b4c4d4f505152',
        'ecb-tbl-192: I=40'),
    ('626d34c9429b37211330986466b94e5f', 'b9ddd29ac6128a6cab121e34a4c62b36',
        '54555657595a5b5c5e5f60616364656668696a6b6d6e6f70',
        'ecb-tbl-192: I=41'),
    ('333c3e6bf00656b088a17e5ff0e7f60a', '6fcddad898f2ce4eff51294f5eaaf5c9',
        '727374757778797a7c7d7e7f81828384868788898b8c8d8e',
        'ecb-tbl-192: I=42'),
    ('687ed0cdc0d2a2bc8c466d05ef9d2891', 'c9a6fe2bf4028080bea6f7fc417bd7e3',
        '90919293959697989a9b9c9d9fa0a1a2a4a5a6a7a9aaabac',
        'ecb-tbl-192: I=43'),
    ('487830e78cc56c1693e64b2a6660c7b6', '6a2026846d8609d60f298a9c0673127f',
        'aeafb0b1b3b4b5b6b8b9babbbdbebfc0c2c3c4c5c7c8c9ca',
        'ecb-tbl-192: I=44'),
    ('7a48d6b7b52b29392aa2072a32b66160', '2cb25c005e26efea44336c4c97a4240b',
        'cccdcecfd1d2d3d4d6d7d8d9dbdcdddee0e1e2e3e5e6e7e8',
        'ecb-tbl-192: I=45'),
    ('907320e64c8c5314d10f8d7a11c8618d', '496967ab8680ddd73d09a0e4c7dcc8aa',
        'eaebecedeff0f1f2f4f5f6f7f9fafbfcfefe010103040506',
        'ecb-tbl-192: I=46'),
    ('b561f2ca2d6e65a4a98341f3ed9ff533', 'd5af94de93487d1f3a8c577cb84a66a4',
        '08090a0b0d0e0f10121314151718191a1c1d1e1f21222324',
        'ecb-tbl-192: I=47'),
    ('df769380d212792d026f049e2e3e48ef', '84bdac569cae2828705f267cc8376e90',
        '262728292b2c2d2e30313233353637383a3b3c3d3f404142',
        'ecb-tbl-192: I=48'),
    ('79f374bc445bdabf8fccb8843d6054c6', 'f7401dda5ad5ab712b7eb5d10c6f99b6',
        '44454647494a4b4c4e4f50515354555658595a5b5d5e5f60',
        'ecb-tbl-192: I=49'),
    ('4e02f1242fa56b05c68dbae8fe44c9d6', '1c9d54318539ebd4c3b5b7e37bf119f0',
        '626364656768696a6c6d6e6f71727374767778797b7c7d7e',
        'ecb-tbl-192: I=50'),
    ('cf73c93cbff57ac635a6f4ad2a4a1545', 'aca572d65fb2764cffd4a6eca090ea0d',
        '80818283858687888a8b8c8d8f90919294959697999a9b9c',
        'ecb-tbl-192: I=51'),
    ('9923548e2875750725b886566784c625', '36d9c627b8c2a886a10ccb36eae3dfbb',
        '9e9fa0a1a3a4a5a6a8a9aaabadaeafb0b2b3b4b5b7b8b9ba',
        'ecb-tbl-192: I=52'),
    ('4888336b723a022c9545320f836a4207', '010edbf5981e143a81d646e597a4a568',
        'bcbdbebfc1c2c3c4c6c7c8c9cbcccdced0d1d2d3d5d6d7d8',
        'ecb-tbl-192: I=53'),
    ('f84d9a5561b0608b1160dee000c41ba8', '8db44d538dc20cc2f40f3067fd298e60',
        'dadbdcdddfe0e1e2e4e5e6e7e9eaebeceeeff0f1f3f4f5f6',
        'ecb-tbl-192: I=54'),
    ('c23192a0418e30a19b45ae3e3625bf22', '930eb53bc71e6ac4b82972bdcd5aafb3',
        'f8f9fafbfdfefe00020304050708090a0c0d0e0f11121314',
        'ecb-tbl-192: I=55'),
    ('b84e0690b28b0025381ad82a15e501a7', '6c42a81edcbc9517ccd89c30c95597b4',
        '161718191b1c1d1e20212223252627282a2b2c2d2f303132',
        'ecb-tbl-192: I=56'),
    ('acef5e5c108876c4f06269f865b8f0b0', 'da389847ad06df19d76ee119c71e1dd3',
        '34353637393a3b3c3e3f40414344454648494a4b4d4e4f50',
        'ecb-tbl-192: I=57'),
    ('0f1b3603e0f5ddea4548246153a5e064', 'e018fdae13d3118f9a5d1a647a3f0462',
        '525354555758595a5c5d5e5f61626364666768696b6c6d6e',
        'ecb-tbl-192: I=58'),
    ('fbb63893450d42b58c6d88cd3c1809e3', '2aa65db36264239d3846180fabdfad20',
        '70717273757677787a7b7c7d7f80818284858687898a8b8c',
        'ecb-tbl-192: I=59'),
    ('4bef736df150259dae0c91354e8a5f92', '1472163e9a4f780f1ceb44b07ecf4fdb',
        '8e8f90919394959698999a9b9d9e9fa0a2a3a4a5a7a8a9aa',
        'ecb-tbl-192: I=60'),
    ('7d2d46242056ef13d3c3fc93c128f4c7', 'c8273fdc8f3a9f72e91097614b62397c',
        'acadaeafb1b2b3b4b6b7b8b9bbbcbdbec0c1c2c3c5c6c7c8',
        'ecb-tbl-192: I=61'),
    ('e9c1ba2df415657a256edb33934680fd', '66c8427dcd733aaf7b3470cb7d976e3f',
        'cacbcccdcfd0d1d2d4d5d6d7d9dadbdcdedfe0e1e3e4e5e6',
        'ecb-tbl-192: I=62'),
    ('e23ee277b0aa0a1dfb81f7527c3514f1', '146131cb17f1424d4f8da91e6f80c1d0',
        'e8e9eaebedeeeff0f2f3f4f5f7f8f9fafcfdfeff01020304',
        'ecb-tbl-192: I=63'),
    ('3e7445b0b63caaf75e4a911e12106b4c', '2610d0ad83659081ae085266a88770dc',
        '060708090b0c0d0e10111213151617181a1b1c1d1f202122',
        'ecb-tbl-192: I=64'),
    ('767774752023222544455a5be6e1e0e3', '38a2b5a974b0575c5d733917fb0d4570',
        '24252627292a2b2c2e2f30313334353638393a3b3d3e3f40',
        'ecb-tbl-192: I=65'),
    ('72737475717e7f7ce9e8ebea696a6b6c', 'e21d401ebc60de20d6c486e4f39a588b',
        '424344454748494a4c4d4e4f51525354565758595b5c5d5e',
        'ecb-tbl-192: I=66'),
    ('dfdedddc25262728c9c8cfcef1eeefec', 'e51d5f88c670b079c0ca1f0c2c4405a2',
        '60616263656667686a6b6c6d6f70717274757677797a7b7c',
        'ecb-tbl-192: I=67'),
    ('fffe0100707776755f5e5d5c7675746b', '246a94788a642fb3d1b823c8762380c8',
        '7e7f80818384858688898a8b8d8e8f90929394959798999a',
        'ecb-tbl-192: I=68'),
    ('e0e1e2e3424140479f9e9190292e2f2c', 'b80c391c5c41a4c3b30c68e0e3d7550f',
        '9c9d9e9fa1a2a3a4a6a7a8a9abacadaeb0b1b2b3b5b6b7b8',
        'ecb-tbl-192: I=69'),
    ('2120272690efeeed3b3a39384e4d4c4b', 'b77c4754fc64eb9a1154a9af0bb1f21c',
        'babbbcbdbfc0c1c2c4c5c6c7c9cacbcccecfd0d1d3d4d5d6',
        'ecb-tbl-192: I=70'),
    ('ecedeeef5350516ea1a0a7a6a3acadae', 'fb554de520d159a06bf219fc7f34a02f',
        'd8d9dadbdddedfe0e2e3e4e5e7e8e9eaecedeeeff1f2f3f4',
        'ecb-tbl-192: I=71'),
    ('32333c3d25222320e9e8ebeacecdccc3', 'a89fba152d76b4927beed160ddb76c57',
        'f6f7f8f9fbfcfdfe00010203050607080a0b0c0d0f101112',
        'ecb-tbl-192: I=72'),
    ('40414243626160678a8bb4b511161714', '5676eab4a98d2e8473b3f3d46424247c',
        '14151617191a1b1c1e1f20212324252628292a2b2d2e2f30',
        'ecb-tbl-192: I=73'),
    ('94959293f5fafbf81f1e1d1c7c7f7e79', '4e8f068bd7ede52a639036ec86c33568',
        '323334353738393a3c3d3e3f41424344464748494b4c4d4e',
        'ecb-tbl-192: I=74'),
    ('bebfbcbd191a1b14cfcec9c8546b6a69', 'f0193c4d7aff1791ee4c07eb4a1824fc',
        '50515253555657585a5b5c5d5f60616264656667696a6b6c',
        'ecb-tbl-192: I=75'),
    ('2c2d3233898e8f8cbbbab9b8333031ce', 'ac8686eeca9ba761afe82d67b928c33f',
        '6e6f70717374757678797a7b7d7e7f80828384858788898a',
        'ecb-tbl-192: I=76'),
    ('84858687bfbcbdba37363938fdfafbf8', '5faf8573e33b145b6a369cd3606ab2c9',
        '8c8d8e8f91929394969798999b9c9d9ea0a1a2a3a5a6a7a8',
        'ecb-tbl-192: I=77'),
    ('828384857669686b909192930b08090e', '31587e9944ab1c16b844ecad0df2e7da',
        'aaabacadafb0b1b2b4b5b6b7b9babbbcbebfc0c1c3c4c5c6',
        'ecb-tbl-192: I=78'),
    ('bebfbcbd9695948b707176779e919093', 'd017fecd91148aba37f6f3068aa67d8a',
        'c8c9cacbcdcecfd0d2d3d4d5d7d8d9dadcdddedfe1e2e3e4',
        'ecb-tbl-192: I=79'),
    ('8b8a85846067666521202322d0d3d2dd', '788ef2f021a73cba2794b616078a8500',
        'e6e7e8e9ebecedeef0f1f2f3f5f6f7f8fafbfcfdfe010002',
        'ecb-tbl-192: I=80'),
    ('76777475f1f2f3f4f8f9e6e777707172', '5d1ef20dced6bcbc12131ac7c54788aa',
        '04050607090a0b0c0e0f10111314151618191a1b1d1e1f20',
        'ecb-tbl-192: I=81'),
    ('a4a5a2a34f404142b4b5b6b727242522', 'b3c8cf961faf9ea05fdde6d1e4d8f663',
        '222324252728292a2c2d2e2f31323334363738393b3c3d3e',
        'ecb-tbl-192: I=82'),
    ('94959697e1e2e3ec16171011839c9d9e', '143075c70605861c7fac6526199e459f',
        '40414243454647484a4b4c4d4f50515254555657595a5b5c',
        'ecb-tbl-192: I=83'),
    ('03023d3c06010003dedfdcddfffcfde2', 'a5ae12eade9a87268d898bfc8fc0252a',
        '5e5f60616364656668696a6b6d6e6f70727374757778797a',
        'ecb-tbl-192: I=84'),
    ('10111213f1f2f3f4cecfc0c1dbdcddde', '0924f7cf2e877a4819f5244a360dcea9',
        '7c7d7e7f81828384868788898b8c8d8e9091929395969798',
        'ecb-tbl-192: I=85'),
    ('67666160724d4c4f1d1c1f1e73707176', '3d9e9635afcc3e291cc7ab3f27d1c99a',
        '9a9b9c9d9fa0a1a2a4a5a6a7a9aaabacaeafb0b1b3b4b5b6',
        'ecb-tbl-192: I=86'),
    ('e6e7e4e5a8abaad584858283909f9e9d', '9d80feebf87510e2b8fb98bb54fd788c',
        'b8b9babbbdbebfc0c2c3c4c5c7c8c9cacccdcecfd1d2d3d4',
        'ecb-tbl-192: I=87'),
    ('71707f7e565150537d7c7f7e6162636c', '5f9d1a082a1a37985f174002eca01309',
        'd6d7d8d9dbdcdddee0e1e2e3e5e6e7e8eaebecedeff0f1f2',
        'ecb-tbl-192: I=88'),
    ('64656667212223245555aaaa03040506', 'a390ebb1d1403930184a44b4876646e4',
        'f4f5f6f7f9fafbfcfefe01010304050608090a0b0d0e0f10',
        'ecb-tbl-192: I=89'),
    ('9e9f9899aba4a5a6cfcecdcc2b28292e', '700fe918981c3195bb6c4bcb46b74e29',
        '121314151718191a1c1d1e1f21222324262728292b2c2d2e',
        'ecb-tbl-192: I=90'),
    ('c7c6c5c4d1d2d3dc626364653a454447', '907984406f7bf2d17fb1eb15b673d747',
        '30313233353637383a3b3c3d3f40414244454647494a4b4c',
        'ecb-tbl-192: I=91'),
    ('f6f7e8e9e0e7e6e51d1c1f1e5b585966', 'c32a956dcfc875c2ac7c7cc8b8cc26e1',
        '4e4f50515354555658595a5b5d5e5f60626364656768696a',
        'ecb-tbl-192: I=92'),
    ('bcbdbebf5d5e5f5868696667f4f3f2f1', '02646e2ebfa9b820cf8424e9b9b6eb51',
        '6c6d6e6f71727374767778797b7c7d7e8081828385868788',
        'ecb-tbl-192: I=93'),
    ('40414647b0afaead9b9a99989b98999e', '621fda3a5bbd54c6d3c685816bd4ead8',
        '8a8b8c8d8f90919294959697999a9b9c9e9fa0a1a3a4a5a6',
        'ecb-tbl-192: I=94'),
    ('69686b6a0201001f0f0e0908b4bbbab9', 'd4e216040426dfaf18b152469bc5ac2f',
        'a8a9aaabadaeafb0b2b3b4b5b7b8b9babcbdbebfc1c2c3c4',
        'ecb-tbl-192: I=95'),
    ('c7c6c9c8d8dfdedd5a5b5859bebdbcb3', '9d0635b9d33b6cdbd71f5d246ea17cc8',
        'c6c7c8c9cbcccdced0d1d2d3d5d6d7d8dadbdcdddfe0e1e2',
        'ecb-tbl-192: I=96'),
    ('dedfdcdd787b7a7dfffee1e0b2b5b4b7', '10abad1bd9bae5448808765583a2cc1a',
        'e4e5e6e7e9eaebeceeeff0f1f3f4f5f6f8f9fafbfdfefe00',
        'ecb-tbl-192: I=97'),
    ('4d4c4b4a606f6e6dd0d1d2d3fbf8f9fe', '6891889e16544e355ff65a793c39c9a8',
        '020304050708090a0c0d0e0f11121314161718191b1c1d1e',
        'ecb-tbl-192: I=98'),
    ('b7b6b5b4d7d4d5dae5e4e3e2e1fefffc', 'cc735582e68072c163cd9ddf46b91279',
        '20212223252627282a2b2c2d2f30313234353637393a3b3c',
        'ecb-tbl-192: I=99'),
    ('cecfb0b1f7f0f1f2aeafacad3e3d3c23', 'c5c68b9aeeb7f878df578efa562f9574',
        '3e3f40414344454648494a4b4d4e4f50525354555758595a',
        'ecb-tbl-192: I=100'),
    ('cacbc8c9cdcecfc812131c1d494e4f4c', '5f4764395a667a47d73452955d0d2ce8',
        '5c5d5e5f61626364666768696b6c6d6e7071727375767778',
        'ecb-tbl-192: I=101'),
    ('9d9c9b9ad22d2c2fb1b0b3b20c0f0e09', '701448331f66106cefddf1eb8267c357',
        '7a7b7c7d7f80818284858687898a8b8c8e8f909193949596',
        'ecb-tbl-192: I=102'),
    ('7a7b787964676659959493924f404142', 'cb3ee56d2e14b4e1941666f13379d657',
        '98999a9b9d9e9fa0a2a3a4a5a7a8a9aaacadaeafb1b2b3b4',
        'ecb-tbl-192: I=103'),
    ('aaaba4a5cec9c8cb1f1e1d1caba8a9a6', '9fe16efd18ab6e1981191851fedb0764',
        'b6b7b8b9bbbcbdbec0c1c2c3c5c6c7c8cacbcccdcfd0d1d2',
        'ecb-tbl-192: I=104'),
    ('93929190282b2a2dc4c5fafb92959497', '3dc9ba24e1b223589b147adceb4c8e48',
        'd4d5d6d7d9dadbdcdedfe0e1e3e4e5e6e8e9eaebedeeeff0',
        'ecb-tbl-192: I=105'),
    ('efeee9e8ded1d0d339383b3a888b8a8d', '1c333032682e7d4de5e5afc05c3e483c',
        'f2f3f4f5f7f8f9fafcfdfeff01020304060708090b0c0d0e',
        'ecb-tbl-192: I=106'),
    ('7f7e7d7ca2a1a0af78797e7f112e2f2c', 'd593cc99a95afef7e92038e05a59d00a',
        '10111213151617181a1b1c1d1f20212224252627292a2b2c',
        'ecb-tbl-192: I=107'),
    ('84859a9b2b2c2d2e868784852625245b', '51e7f96f53b4353923452c222134e1ec',
        '2e2f30313334353638393a3b3d3e3f40424344454748494a',
        'ecb-tbl-192: I=108'),
    ('b0b1b2b3070405026869666710171615', '4075b357a1a2b473400c3b25f32f81a4',
        '4c4d4e4f51525354565758595b5c5d5e6061626365666768',
        'ecb-tbl-192: I=109'),
    ('acadaaabbda2a3a00d0c0f0e595a5b5c', '302e341a3ebcd74f0d55f61714570284',
        '6a6b6c6d6f70717274757677797a7b7c7e7f808183848586',
        'ecb-tbl-192: I=110'),
    ('121310115655544b5253545569666764', '57abdd8231280da01c5042b78cf76522',
        '88898a8b8d8e8f90929394959798999a9c9d9e9fa1a2a3a4',
        'ecb-tbl-192: I=111'),
    ('dedfd0d166616063eaebe8e94142434c', '17f9ea7eea17ac1adf0e190fef799e92',
        'a6a7a8a9abacadaeb0b1b2b3b5b6b7b8babbbcbdbfc0c1c2',
        'ecb-tbl-192: I=112'),
    ('dbdad9d81417161166677879e0e7e6e5', '2e1bdd563dd87ee5c338dd6d098d0a7a',
        'c4c5c6c7c9cacbcccecfd0d1d3d4d5d6d8d9dadbdddedfe0',
        'ecb-tbl-192: I=113'),
    ('6a6b6c6de0efeeed2b2a2928c0c3c2c5', 'eb869996e6f8bfb2bfdd9e0c4504dbb2',
        'e2e3e4e5e7e8e9eaecedeeeff1f2f3f4f6f7f8f9fbfcfdfe',
        'ecb-tbl-192: I=114'),
    ('b1b0b3b21714151a1a1b1c1d5649484b', 'c2e01549e9decf317468b3e018c61ba8',
        '00010203050607080a0b0c0d0f10111214151617191a1b1c',
        'ecb-tbl-192: I=115'),
    ('39380706a3a4a5a6c4c5c6c77271706f', '8da875d033c01dd463b244a1770f4a22',
        '1e1f20212324252628292a2b2d2e2f30323334353738393a',
        'ecb-tbl-192: I=116'),
    ('5c5d5e5f1013121539383736e2e5e4e7', '8ba0dcf3a186844f026d022f8839d696',
        '3c3d3e3f41424344464748494b4c4d4e5051525355565758',
        'ecb-tbl-192: I=117'),
    ('43424544ead5d4d72e2f2c2d64676661', 'e9691ff9a6cc6970e51670a0fd5b88c1',
        '5a5b5c5d5f60616264656667696a6b6c6e6f707173747576',
        'ecb-tbl-192: I=118'),
    ('55545756989b9a65f8f9feff18171615', 'f2baec06faeed30f88ee63ba081a6e5b',
        '78797a7b7d7e7f80828384858788898a8c8d8e8f91929394',
        'ecb-tbl-192: I=119'),
    ('05040b0a525554573c3d3e3f4a494847', '9c39d4c459ae5753394d6094adc21e78',
        '969798999b9c9d9ea0a1a2a3a5a6a7a8aaabacadafb0b1b2',
        'ecb-tbl-192: I=120'),
    ('14151617595a5b5c8584fbfa8e89888b', '6345b532a11904502ea43ba99c6bd2b2',
        'b4b5b6b7b9babbbcbebfc0c1c3c4c5c6c8c9cacbcdcecfd0',
        'ecb-tbl-192: I=121'),
    ('7c7d7a7bfdf2f3f029282b2a51525354', '5ffae3061a95172e4070cedce1e428c8',
        'd2d3d4d5d7d8d9dadcdddedfe1e2e3e4e6e7e8e9ebecedee',
        'ecb-tbl-192: I=122'),
    ('38393a3b1e1d1c1341404746c23d3c3e', '0a4566be4cdf9adce5dec865b5ab34cd',
        'f0f1f2f3f5f6f7f8fafbfcfdfe01000204050607090a0b0c',
        'ecb-tbl-192: I=123'),
    ('8d8c939240474645818083827c7f7e41', 'ca17fcce79b7404f2559b22928f126fb',
        '0e0f10111314151618191a1b1d1e1f20222324252728292a',
        'ecb-tbl-192: I=124'),
    ('3b3a39381a19181f32333c3d45424340', '97ca39b849ed73a6470a97c821d82f58',
        '2c2d2e2f31323334363738393b3c3d3e4041424345464748',
        'ecb-tbl-192: I=125'),
    ('f0f1f6f738272625828380817f7c7d7a', '8198cb06bc684c6d3e9b7989428dcf7a',
        '4a4b4c4d4f50515254555657595a5b5c5e5f606163646566',
        'ecb-tbl-192: I=126'),
    ('89888b8a0407061966676061141b1a19', 'f53c464c705ee0f28d9a4c59374928bd',
        '68696a6b6d6e6f70727374757778797a7c7d7e7f81828384',
        'ecb-tbl-192: I=127'),
    ('d3d2dddcaaadacaf9c9d9e9fe8ebeae5', '9adb3d4cca559bb98c3e2ed73dbf1154',
        '868788898b8c8d8e90919293959697989a9b9c9d9fa0a1a2',
        'ecb-tbl-192: I=128'),

    # ecb_tbl.txt, KEYSIZE=256
    ('834eadfccac7e1b30664b1aba44815ab', '1946dabf6a03a2a2c3d0b05080aed6fc',
        '00010203050607080a0b0c0d0f10111214151617191a1b1c1e1f202123242526',
        'ecb-tbl-256: I=1'),
    ('d9dc4dba3021b05d67c0518f72b62bf1', '5ed301d747d3cc715445ebdec62f2fb4',
        '28292a2b2d2e2f30323334353738393a3c3d3e3f41424344464748494b4c4d4e',
        'ecb-tbl-256: I=2'),
    ('a291d86301a4a739f7392173aa3c604c', '6585c8f43d13a6beab6419fc5935b9d0',
        '50515253555657585a5b5c5d5f60616264656667696a6b6c6e6f707173747576',
        'ecb-tbl-256: I=3'),
    ('4264b2696498de4df79788a9f83e9390', '2a5b56a596680fcc0e05f5e0f151ecae',
        '78797a7b7d7e7f80828384858788898a8c8d8e8f91929394969798999b9c9d9e',
        'ecb-tbl-256: I=4'),
    ('ee9932b3721804d5a83ef5949245b6f6', 'f5d6ff414fd2c6181494d20c37f2b8c4',
        'a0a1a2a3a5a6a7a8aaabacadafb0b1b2b4b5b6b7b9babbbcbebfc0c1c3c4c5c6',
        'ecb-tbl-256: I=5'),
    ('e6248f55c5fdcbca9cbbb01c88a2ea77', '85399c01f59fffb5204f19f8482f00b8',
        'c8c9cacbcdcecfd0d2d3d4d5d7d8d9dadcdddedfe1e2e3e4e6e7e8e9ebecedee',
        'ecb-tbl-256: I=6'),
    ('b8358e41b9dff65fd461d55a99266247', '92097b4c88a041ddf98144bc8d22e8e7',
        'f0f1f2f3f5f6f7f8fafbfcfdfe01000204050607090a0b0c0e0f101113141516',
        'ecb-tbl-256: I=7'),
    ('f0e2d72260af58e21e015ab3a4c0d906', '89bd5b73b356ab412aef9f76cea2d65c',
        '18191a1b1d1e1f20222324252728292a2c2d2e2f31323334363738393b3c3d3e',
        'ecb-tbl-256: I=8'),
    ('475b8b823ce8893db3c44a9f2a379ff7', '2536969093c55ff9454692f2fac2f530',
        '40414243454647484a4b4c4d4f50515254555657595a5b5c5e5f606163646566',
        'ecb-tbl-256: I=9'),
    ('688f5281945812862f5f3076cf80412f', '07fc76a872843f3f6e0081ee9396d637',
        '68696a6b6d6e6f70727374757778797a7c7d7e7f81828384868788898b8c8d8e',
        'ecb-tbl-256: I=10'),
    ('08d1d2bc750af553365d35e75afaceaa', 'e38ba8ec2aa741358dcc93e8f141c491',
        '90919293959697989a9b9c9d9fa0a1a2a4a5a6a7a9aaabacaeafb0b1b3b4b5b6',
        'ecb-tbl-256: I=11'),
    ('8707121f47cc3efceca5f9a8474950a1', 'd028ee23e4a89075d0b03e868d7d3a42',
        'b8b9babbbdbebfc0c2c3c4c5c7c8c9cacccdcecfd1d2d3d4d6d7d8d9dbdcddde',
        'ecb-tbl-256: I=12'),
    ('e51aa0b135dba566939c3b6359a980c5', '8cd9423dfc459e547155c5d1d522e540',
        'e0e1e2e3e5e6e7e8eaebecedeff0f1f2f4f5f6f7f9fafbfcfefe010103040506',
        'ecb-tbl-256: I=13'),
    ('069a007fc76a459f98baf917fedf9521', '080e9517eb1677719acf728086040ae3',
        '08090a0b0d0e0f10121314151718191a1c1d1e1f21222324262728292b2c2d2e',
        'ecb-tbl-256: I=14'),
    ('726165c1723fbcf6c026d7d00b091027', '7c1700211a3991fc0ecded0ab3e576b0',
        '30313233353637383a3b3c3d3f40414244454647494a4b4c4e4f505153545556',
        'ecb-tbl-256: I=15'),
    ('d7c544de91d55cfcde1f84ca382200ce', 'dabcbcc855839251db51e224fbe87435',
        '58595a5b5d5e5f60626364656768696a6c6d6e6f71727374767778797b7c7d7e',
        'ecb-tbl-256: I=16'),
    ('fed3c9a161b9b5b2bd611b41dc9da357', '68d56fad0406947a4dd27a7448c10f1d',
        '80818283858687888a8b8c8d8f90919294959697999a9b9c9e9fa0a1a3a4a5a6',
        'ecb-tbl-256: I=17'),
    ('4f634cdc6551043409f30b635832cf82', 'da9a11479844d1ffee24bbf3719a9925',
        'a8a9aaabadaeafb0b2b3b4b5b7b8b9babcbdbebfc1c2c3c4c6c7c8c9cbcccdce',
        'ecb-tbl-256: I=18'),
    ('109ce98db0dfb36734d9f3394711b4e6', '5e4ba572f8d23e738da9b05ba24b8d81',
        'd0d1d2d3d5d6d7d8dadbdcdddfe0e1e2e4e5e6e7e9eaebeceeeff0f1f3f4f5f6',
        'ecb-tbl-256: I=19'),
    ('4ea6dfaba2d8a02ffdffa89835987242', 'a115a2065d667e3f0b883837a6e903f8',
        '70717273757677787a7b7c7d7f80818284858687898a8b8c8e8f909193949596',
        'ecb-tbl-256: I=20'),
    ('5ae094f54af58e6e3cdbf976dac6d9ef', '3e9e90dc33eac2437d86ad30b137e66e',
        '98999a9b9d9e9fa0a2a3a4a5a7a8a9aaacadaeafb1b2b3b4b6b7b8b9bbbcbdbe',
        'ecb-tbl-256: I=21'),
    ('764d8e8e0f29926dbe5122e66354fdbe', '01ce82d8fbcdae824cb3c48e495c3692',
        'c0c1c2c3c5c6c7c8cacbcccdcfd0d1d2d4d5d6d7d9dadbdcdedfe0e1e3e4e5e6',
        'ecb-tbl-256: I=22'),
    ('3f0418f888cdf29a982bf6b75410d6a9', '0c9cff163ce936faaf083cfd3dea3117',
        'e8e9eaebedeeeff0f2f3f4f5f7f8f9fafcfdfeff01020304060708090b0c0d0e',
        'ecb-tbl-256: I=23'),
    ('e4a3e7cb12cdd56aa4a75197a9530220', '5131ba9bd48f2bba85560680df504b52',
        '10111213151617181a1b1c1d1f20212224252627292a2b2c2e2f303133343536',
        'ecb-tbl-256: I=24'),
    ('211677684aac1ec1a160f44c4ebf3f26', '9dc503bbf09823aec8a977a5ad26ccb2',
        '38393a3b3d3e3f40424344454748494a4c4d4e4f51525354565758595b5c5d5e',
        'ecb-tbl-256: I=25'),
    ('d21e439ff749ac8f18d6d4b105e03895', '9a6db0c0862e506a9e397225884041d7',
        '60616263656667686a6b6c6d6f70717274757677797a7b7c7e7f808183848586',
        'ecb-tbl-256: I=26'),
    ('d9f6ff44646c4725bd4c0103ff5552a7', '430bf9570804185e1ab6365fc6a6860c',
        '88898a8b8d8e8f90929394959798999a9c9d9e9fa1a2a3a4a6a7a8a9abacadae',
        'ecb-tbl-256: I=27'),
    ('0b1256c2a00b976250cfc5b0c37ed382', '3525ebc02f4886e6a5a3762813e8ce8a',
        'b0b1b2b3b5b6b7b8babbbcbdbfc0c1c2c4c5c6c7c9cacbcccecfd0d1d3d4d5d6',
        'ecb-tbl-256: I=28'),
    ('b056447ffc6dc4523a36cc2e972a3a79', '07fa265c763779cce224c7bad671027b',
        'd8d9dadbdddedfe0e2e3e4e5e7e8e9eaecedeeeff1f2f3f4f6f7f8f9fbfcfdfe',
        'ecb-tbl-256: I=29'),
    ('5e25ca78f0de55802524d38da3fe4456', 'e8b72b4e8be243438c9fff1f0e205872',
        '00010203050607080a0b0c0d0f10111214151617191a1b1c1e1f202123242526',
        'ecb-tbl-256: I=30'),
    ('a5bcf4728fa5eaad8567c0dc24675f83', '109d4f999a0e11ace1f05e6b22cbcb50',
        '28292a2b2d2e2f30323334353738393a3c3d3e3f41424344464748494b4c4d4e',
        'ecb-tbl-256: I=31'),
    ('814e59f97ed84646b78b2ca022e9ca43', '45a5e8d4c3ed58403ff08d68a0cc4029',
        '50515253555657585a5b5c5d5f60616264656667696a6b6c6e6f707173747576',
        'ecb-tbl-256: I=32'),
    ('15478beec58f4775c7a7f5d4395514d7', '196865964db3d417b6bd4d586bcb7634',
        '78797a7b7d7e7f80828384858788898a8c8d8e8f91929394969798999b9c9d9e',
        'ecb-tbl-256: I=33'),
    ('253548ffca461c67c8cbc78cd59f4756', '60436ad45ac7d30d99195f815d98d2ae',
        'a0a1a2a3a5a6a7a8aaabacadafb0b1b2b4b5b6b7b9babbbcbebfc0c1c3c4c5c6',
        'ecb-tbl-256: I=34'),
    ('fd7ad8d73b9b0f8cc41600640f503d65', 'bb07a23f0b61014b197620c185e2cd75',
        'c8c9cacbcdcecfd0d2d3d4d5d7d8d9dadcdddedfe1e2e3e4e6e7e8e9ebecedee',
        'ecb-tbl-256: I=35'),
    ('06199de52c6cbf8af954cd65830bcd56', '5bc0b2850129c854423aff0751fe343b',
        'f0f1f2f3f5f6f7f8fafbfcfdfe01000204050607090a0b0c0e0f101113141516',
        'ecb-tbl-256: I=36'),
    ('f17c4ffe48e44c61bd891e257e725794', '7541a78f96738e6417d2a24bd2beca40',
        '18191a1b1d1e1f20222324252728292a2c2d2e2f31323334363738393b3c3d3e',
        'ecb-tbl-256: I=37'),
    ('9a5b4a402a3e8a59be6bf5cd8154f029', 'b0a303054412882e464591f1546c5b9e',
        '40414243454647484a4b4c4d4f50515254555657595a5b5c5e5f606163646566',
        'ecb-tbl-256: I=38'),
    ('79bd40b91a7e07dc939d441782ae6b17', '778c06d8a355eeee214fcea14b4e0eef',
        '68696a6b6d6e6f70727374757778797a7c7d7e7f81828384868788898b8c8d8e',
        'ecb-tbl-256: I=39'),
    ('d8ceaaf8976e5fbe1012d8c84f323799', '09614206d15cbace63227d06db6beebb',
        '90919293959697989a9b9c9d9fa0a1a2a4a5a6a7a9aaabacaeafb0b1b3b4b5b6',
        'ecb-tbl-256: I=40'),
    ('3316e2751e2e388b083da23dd6ac3fbe', '41b97fb20e427a9fdbbb358d9262255d',
        'b8b9babbbdbebfc0c2c3c4c5c7c8c9cacccdcecfd1d2d3d4d6d7d8d9dbdcddde',
        'ecb-tbl-256: I=41'),
    ('8b7cfbe37de7dca793521819242c5816', 'c1940f703d845f957652c2d64abd7adf',
        'e0e1e2e3e5e6e7e8eaebecedeff0f1f2f4f5f6f7f9fafbfcfefe010103040506',
        'ecb-tbl-256: I=42'),
    ('f23f033c0eebf8ec55752662fd58ce68', 'd2d44fcdae5332343366db297efcf21b',
        '08090a0b0d0e0f10121314151718191a1c1d1e1f21222324262728292b2c2d2e',
        'ecb-tbl-256: I=43'),
    ('59eb34f6c8bdbacc5fc6ad73a59a1301', 'ea8196b79dbe167b6aa9896e287eed2b',
        '30313233353637383a3b3c3d3f40414244454647494a4b4c4e4f505153545556',
        'ecb-tbl-256: I=44'),
    ('dcde8b6bd5cf7cc22d9505e3ce81261a', 'd6b0b0c4ba6c7dbe5ed467a1e3f06c2d',
        '58595a5b5d5e5f60626364656768696a6c6d6e6f71727374767778797b7c7d7e',
        'ecb-tbl-256: I=45'),
    ('e33cf7e524fed781e7042ff9f4b35dc7', 'ec51eb295250c22c2fb01816fb72bcae',
        '80818283858687888a8b8c8d8f90919294959697999a9b9c9e9fa0a1a3a4a5a6',
        'ecb-tbl-256: I=46'),
    ('27963c8facdf73062867d164df6d064c', 'aded6630a07ce9c7408a155d3bd0d36f',
        'a8a9aaabadaeafb0b2b3b4b5b7b8b9babcbdbebfc1c2c3c4c6c7c8c9cbcccdce',
        'ecb-tbl-256: I=47'),
    ('77b1ce386b551b995f2f2a1da994eef8', '697c9245b9937f32f5d1c82319f0363a',
        'd0d1d2d3d5d6d7d8dadbdcdddfe0e1e2e4e5e6e7e9eaebeceeeff0f1f3f4f5f6',
        'ecb-tbl-256: I=48'),
    ('f083388b013679efcf0bb9b15d52ae5c', 'aad5ad50c6262aaec30541a1b7b5b19c',
        'f8f9fafbfdfefe00020304050708090a0c0d0e0f11121314161718191b1c1d1e',
        'ecb-tbl-256: I=49'),
    ('c5009e0dab55db0abdb636f2600290c8', '7d34b893855341ec625bd6875ac18c0d',
        '20212223252627282a2b2c2d2f30313234353637393a3b3c3e3f404143444546',
        'ecb-tbl-256: I=50'),
    ('7804881e26cd532d8514d3683f00f1b9', '7ef05105440f83862f5d780e88f02b41',
        '48494a4b4d4e4f50525354555758595a5c5d5e5f61626364666768696b6c6d6e',
        'ecb-tbl-256: I=51'),
    ('46cddcd73d1eb53e675ca012870a92a3', 'c377c06403382061af2c9c93a8e70df6',
        '70717273757677787a7b7c7d7f80818284858687898a8b8c8e8f909193949596',
        'ecb-tbl-256: I=52'),
    ('a9fb44062bb07fe130a8e8299eacb1ab', '1dbdb3ffdc052dacc83318853abc6de5',
        '98999a9b9d9e9fa0a2a3a4a5a7a8a9aaacadaeafb1b2b3b4b6b7b8b9bbbcbdbe',
        'ecb-tbl-256: I=53'),
    ('2b6ff8d7a5cc3a28a22d5a6f221af26b', '69a6eab00432517d0bf483c91c0963c7',
        'c0c1c2c3c5c6c7c8cacbcccdcfd0d1d2d4d5d6d7d9dadbdcdedfe0e1e3e4e5e6',
        'ecb-tbl-256: I=54'),
    ('1a9527c29b8add4b0e3e656dbb2af8b4', '0797f41dc217c80446e1d514bd6ab197',
        'e8e9eaebedeeeff0f2f3f4f5f7f8f9fafcfdfeff01020304060708090b0c0d0e',
        'ecb-tbl-256: I=55'),
    ('7f99cf2c75244df015eb4b0c1050aeae', '9dfd76575902a637c01343c58e011a03',
        '10111213151617181a1b1c1d1f20212224252627292a2b2c2e2f303133343536',
        'ecb-tbl-256: I=56'),
    ('e84ff85b0d9454071909c1381646c4ed', 'acf4328ae78f34b9fa9b459747cc2658',
        '38393a3b3d3e3f40424344454748494a4c4d4e4f51525354565758595b5c5d5e',
        'ecb-tbl-256: I=57'),
    ('89afd40f99521280d5399b12404f6db4', 'b0479aea12bac4fe2384cf98995150c6',
        '60616263656667686a6b6c6d6f70717274757677797a7b7c7e7f808183848586',
        'ecb-tbl-256: I=58'),
    ('a09ef32dbc5119a35ab7fa38656f0329', '9dd52789efe3ffb99f33b3da5030109a',
        '88898a8b8d8e8f90929394959798999a9c9d9e9fa1a2a3a4a6a7a8a9abacadae',
        'ecb-tbl-256: I=59'),
    ('61773457f068c376c7829b93e696e716', 'abbb755e4621ef8f1214c19f649fb9fd',
        'b0b1b2b3b5b6b7b8babbbcbdbfc0c1c2c4c5c6c7c9cacbcccecfd0d1d3d4d5d6',
        'ecb-tbl-256: I=60'),
    ('a34f0cae726cce41dd498747d891b967', 'da27fb8174357bce2bed0e7354f380f9',
        'd8d9dadbdddedfe0e2e3e4e5e7e8e9eaecedeeeff1f2f3f4f6f7f8f9fbfcfdfe',
        'ecb-tbl-256: I=61'),
    ('856f59496c7388ee2d2b1a27b7697847', 'c59a0663f0993838f6e5856593bdc5ef',
        '00010203050607080a0b0c0d0f10111214151617191a1b1c1e1f202123242526',
        'ecb-tbl-256: I=62'),
    ('cb090c593ef7720bd95908fb93b49df4', 'ed60b264b5213e831607a99c0ce5e57e',
        '28292a2b2d2e2f30323334353738393a3c3d3e3f41424344464748494b4c4d4e',
        'ecb-tbl-256: I=63'),
    ('a0ac75cd2f1923d460fc4d457ad95baf', 'e50548746846f3eb77b8c520640884ed',
        '50515253555657585a5b5c5d5f60616264656667696a6b6c6e6f707173747576',
        'ecb-tbl-256: I=64'),
    ('2a2b282974777689e8e9eeef525d5c5f', '28282cc7d21d6a2923641e52d188ef0c',
        '78797a7b7d7e7f80828384858788898a8c8d8e8f91929394969798999b9c9d9e',
        'ecb-tbl-256: I=65'),
    ('909192939390919e0f0e09089788898a', '0dfa5b02abb18e5a815305216d6d4f8e',
        'a0a1a2a3a5a6a7a8aaabacadafb0b1b2b4b5b6b7b9babbbcbebfc0c1c3c4c5c6',
        'ecb-tbl-256: I=66'),
    ('777675748d8e8f907170777649464744', '7359635c0eecefe31d673395fb46fb99',
        'c8c9cacbcdcecfd0d2d3d4d5d7d8d9dadcdddedfe1e2e3e4e6e7e8e9ebecedee',
        'ecb-tbl-256: I=67'),
    ('717073720605040b2d2c2b2a05fafbf9', '73c679f7d5aef2745c9737bb4c47fb36',
        'f0f1f2f3f5f6f7f8fafbfcfdfe01000204050607090a0b0c0e0f101113141516',
        'ecb-tbl-256: I=68'),
    ('64656667fefdfcc31b1a1d1ca5aaaba8', 'b192bd472a4d2eafb786e97458967626',
        '18191a1b1d1e1f20222324252728292a2c2d2e2f31323334363738393b3c3d3e',
        'ecb-tbl-256: I=69'),
    ('dbdad9d86a696867b5b4b3b2c8d7d6d5', '0ec327f6c8a2b147598ca3fde61dc6a4',
        '40414243454647484a4b4c4d4f50515254555657595a5b5c5e5f606163646566',
        'ecb-tbl-256: I=70'),
    ('5c5d5e5fe3e0e1fe31303736333c3d3e', 'fc418eb3c41b859b38d4b6f646629729',
        '68696a6b6d6e6f70727374757778797a7c7d7e7f81828384868788898b8c8d8e',
        'ecb-tbl-256: I=71'),
    ('545556574b48494673727574546b6a69', '30249e5ac282b1c981ea64b609f3a154',
        '90919293959697989a9b9c9d9fa0a1a2a4a5a6a7a9aaabacaeafb0b1b3b4b5b6',
        'ecb-tbl-256: I=72'),
    ('ecedeeefc6c5c4bb56575051f5fafbf8', '5e6e08646d12150776bb43c2d78a9703',
        'b8b9babbbdbebfc0c2c3c4c5c7c8c9cacccdcecfd1d2d3d4d6d7d8d9dbdcddde',
        'ecb-tbl-256: I=73'),
    ('464744452724252ac9c8cfced2cdcccf', 'faeb3d5de652cd3447dceb343f30394a',
        'e0e1e2e3e5e6e7e8eaebecedeff0f1f2f4f5f6f7f9fafbfcfefe010103040506',
        'ecb-tbl-256: I=74'),
    ('e6e7e4e54142435c878681801c131211', 'a8e88706823f6993ef80d05c1c7b2cf0',
        '08090a0b0d0e0f10121314151718191a1c1d1e1f21222324262728292b2c2d2e',
        'ecb-tbl-256: I=75'),
    ('72737071cfcccdc2f9f8fffe710e0f0c', '8ced86677e6e00a1a1b15968f2d3cce6',
        '30313233353637383a3b3c3d3f40414244454647494a4b4c4e4f505153545556',
        'ecb-tbl-256: I=76'),
    ('505152537370714ec3c2c5c4010e0f0c', '9fc7c23858be03bdebb84e90db6786a9',
        '58595a5b5d5e5f60626364656768696a6c6d6e6f71727374767778797b7c7d7e',
        'ecb-tbl-256: I=77'),
    ('a8a9aaab5c5f5e51aeafa8a93d222320', 'b4fbd65b33f70d8cf7f1111ac4649c36',
        '80818283858687888a8b8c8d8f90919294959697999a9b9c9e9fa0a1a3a4a5a6',
        'ecb-tbl-256: I=78'),
    ('dedfdcddf6f5f4eb10111617fef1f0f3', 'c5c32d5ed03c4b53cc8c1bd0ef0dbbf6',
        'a8a9aaabadaeafb0b2b3b4b5b7b8b9babcbdbebfc1c2c3c4c6c7c8c9cbcccdce',
        'ecb-tbl-256: I=79'),
    ('bdbcbfbe5e5d5c530b0a0d0cfac5c4c7', 'd1a7f03b773e5c212464b63709c6a891',
        'd0d1d2d3d5d6d7d8dadbdcdddfe0e1e2e4e5e6e7e9eaebeceeeff0f1f3f4f5f6',
        'ecb-tbl-256: I=80'),
    ('8a8b8889050606f8f4f5f2f3636c6d6e', '6b7161d8745947ac6950438ea138d028',
        'f8f9fafbfdfefe00020304050708090a0c0d0e0f11121314161718191b1c1d1e',
        'ecb-tbl-256: I=81'),
    ('a6a7a4a54d4e4f40b2b3b4b539262724', 'fd47a9f7e366ee7a09bc508b00460661',
        '20212223252627282a2b2c2d2f30313234353637393a3b3c3e3f404143444546',
        'ecb-tbl-256: I=82'),
    ('9c9d9e9fe9eaebf40e0f08099b949596', '00d40b003dc3a0d9310b659b98c7e416',
        '48494a4b4d4e4f50525354555758595a5c5d5e5f61626364666768696b6c6d6e',
        'ecb-tbl-256: I=83'),
    ('2d2c2f2e1013121dcccdcacbed121310', 'eea4c79dcc8e2bda691f20ac48be0717',
        '70717273757677787a7b7c7d7f80818284858687898a8b8c8e8f909193949596',
        'ecb-tbl-256: I=84'),
    ('f4f5f6f7edeeefd0eaebecedf7f8f9fa', 'e78f43b11c204403e5751f89d05a2509',
        '98999a9b9d9e9fa0a2a3a4a5a7a8a9aaacadaeafb1b2b3b4b6b7b8b9bbbcbdbe',
        'ecb-tbl-256: I=85'),
    ('3d3c3f3e282b2a2573727574150a0b08', 'd0f0e3d1f1244bb979931e38dd1786ef',
        'c0c1c2c3c5c6c7c8cacbcccdcfd0d1d2d4d5d6d7d9dadbdcdedfe0e1e3e4e5e6',
        'ecb-tbl-256: I=86'),
    ('b6b7b4b5f8fbfae5b4b5b2b3a0afaead', '042e639dc4e1e4dde7b75b749ea6f765',
        'e8e9eaebedeeeff0f2f3f4f5f7f8f9fafcfdfeff01020304060708090b0c0d0e',
        'ecb-tbl-256: I=87'),
    ('b7b6b5b4989b9a95878681809ba4a5a6', 'bc032fdd0efe29503a980a7d07ab46a8',
        '10111213151617181a1b1c1d1f20212224252627292a2b2c2e2f303133343536',
        'ecb-tbl-256: I=88'),
    ('a8a9aaabe5e6e798e9e8efee4748494a', '0c93ac949c0da6446effb86183b6c910',
        '38393a3b3d3e3f40424344454748494a4c4d4e4f51525354565758595b5c5d5e',
        'ecb-tbl-256: I=89'),
    ('ecedeeefd9dadbd4b9b8bfbe657a7b78', 'e0d343e14da75c917b4a5cec4810d7c2',
        '60616263656667686a6b6c6d6f70717274757677797a7b7c7e7f808183848586',
        'ecb-tbl-256: I=90'),
    ('7f7e7d7c696a6b74cacbcccd929d9c9f', '0eafb821748408279b937b626792e619',
        '88898a8b8d8e8f90929394959798999a9c9d9e9fa1a2a3a4a6a7a8a9abacadae',
        'ecb-tbl-256: I=91'),
    ('08090a0b0605040bfffef9f8b9c6c7c4', 'fa1ac6e02d23b106a1fef18b274a553f',
        'b0b1b2b3b5b6b7b8babbbcbdbfc0c1c2c4c5c6c7c9cacbcccecfd0d1d3d4d5d6',
        'ecb-tbl-256: I=92'),
    ('08090a0bf1f2f3ccfcfdfafb68676665', '0dadfe019cd12368075507df33c1a1e9',
        'd8d9dadbdddedfe0e2e3e4e5e7e8e9eaecedeeeff1f2f3f4f6f7f8f9fbfcfdfe',
        'ecb-tbl-256: I=93'),
    ('cacbc8c93a393837050403020d121310', '3a0879b414465d9ffbaf86b33a63a1b9',
        '00010203050607080a0b0c0d0f10111214151617191a1b1c1e1f202123242526',
        'ecb-tbl-256: I=94'),
    ('e9e8ebea8281809f8f8e8988343b3a39', '62199fadc76d0be1805d3ba0b7d914bf',
        '28292a2b2d2e2f30323334353738393a3c3d3e3f41424344464748494b4c4d4e',
        'ecb-tbl-256: I=95'),
    ('515053524645444bd0d1d6d7340b0a09', '1b06d6c5d333e742730130cf78e719b4',
        '50515253555657585a5b5c5d5f60616264656667696a6b6c6e6f707173747576',
        'ecb-tbl-256: I=96'),
    ('42434041ecefee1193929594c6c9c8cb', 'f1f848824c32e9dcdcbf21580f069329',
        '78797a7b7d7e7f80828384858788898a8c8d8e8f91929394969798999b9c9d9e',
        'ecb-tbl-256: I=97'),
    ('efeeedecc2c1c0cf76777071455a5b58', '1a09050cbd684f784d8e965e0782f28a',
        'a0a1a2a3a5a6a7a8aaabacadafb0b1b2b4b5b6b7b9babbbcbebfc0c1c3c4c5c6',
        'ecb-tbl-256: I=98'),
    ('5f5e5d5c3f3c3d221d1c1b1a19161714', '79c2969e7ded2ba7d088f3f320692360',
        'c8c9cacbcdcecfd0d2d3d4d5d7d8d9dadcdddedfe1e2e3e4e6e7e8e9ebecedee',
        'ecb-tbl-256: I=99'),
    ('000102034142434c1c1d1a1b8d727371', '091a658a2f7444c16accb669450c7b63',
        'f0f1f2f3f5f6f7f8fafbfcfdfe01000204050607090a0b0c0e0f101113141516',
        'ecb-tbl-256: I=100'),
    ('8e8f8c8db1b2b38c56575051050a0b08', '97c1e3a72cca65fa977d5ed0e8a7bbfc',
        '18191a1b1d1e1f20222324252728292a2c2d2e2f31323334363738393b3c3d3e',
        'ecb-tbl-256: I=101'),
    ('a7a6a5a4e8ebeae57f7e7978cad5d4d7', '70c430c6db9a17828937305a2df91a2a',
        '40414243454647484a4b4c4d4f50515254555657595a5b5c5e5f606163646566',
        'ecb-tbl-256: I=102'),
    ('8a8b888994979689454443429f909192', '629553457fbe2479098571c7c903fde8',
        '68696a6b6d6e6f70727374757778797a7c7d7e7f81828384868788898b8c8d8e',
        'ecb-tbl-256: I=103'),
    ('8c8d8e8fe0e3e2ed45444342f1cecfcc', 'a25b25a61f612669e7d91265c7d476ba',
        '90919293959697989a9b9c9d9fa0a1a2a4a5a6a7a9aaabacaeafb0b1b3b4b5b6',
        'ecb-tbl-256: I=104'),
    ('fffefdfc4c4f4e31d8d9dedfb6b9b8bb', 'eb7e4e49b8ae0f024570dda293254fed',
        'b8b9babbbdbebfc0c2c3c4c5c7c8c9cacccdcecfd1d2d3d4d6d7d8d9dbdcddde',
        'ecb-tbl-256: I=105'),
    ('fdfcfffecccfcec12f2e29286679787b', '38fe15d61cca84516e924adce5014f67',
        'e0e1e2e3e5e6e7e8eaebecedeff0f1f2f4f5f6f7f9fafbfcfefe010103040506',
        'ecb-tbl-256: I=106'),
    ('67666564bab9b8a77071767719161714', '3ad208492249108c9f3ebeb167ad0583',
        '08090a0b0d0e0f10121314151718191a1c1d1e1f21222324262728292b2c2d2e',
        'ecb-tbl-256: I=107'),
    ('9a9b98992d2e2f2084858283245b5a59', '299ba9f9bf5ab05c3580fc26edd1ed12',
        '30313233353637383a3b3c3d3f40414244454647494a4b4c4e4f505153545556',
        'ecb-tbl-256: I=108'),
    ('a4a5a6a70b0809365c5d5a5b2c232221', '19dc705b857a60fb07717b2ea5717781',
        '58595a5b5d5e5f60626364656768696a6c6d6e6f71727374767778797b7c7d7e',
        'ecb-tbl-256: I=109'),
    ('464744455754555af3f2f5f4afb0b1b2', 'ffc8aeb885b5efcad06b6dbebf92e76b',
        '80818283858687888a8b8c8d8f90919294959697999a9b9c9e9fa0a1a3a4a5a6',
        'ecb-tbl-256: I=110'),
    ('323330317675746b7273747549464744', 'f58900c5e0b385253ff2546250a0142b',
        'a8a9aaabadaeafb0b2b3b4b5b7b8b9babcbdbebfc1c2c3c4c6c7c8c9cbcccdce',
        'ecb-tbl-256: I=111'),
    ('a8a9aaab181b1a15808186872b141516', '2ee67b56280bc462429cee6e3370cbc1',
        'd0d1d2d3d5d6d7d8dadbdcdddfe0e1e2e4e5e6e7e9eaebeceeeff0f1f3f4f5f6',
        'ecb-tbl-256: I=112'),
    ('e7e6e5e4202323ddaaabacad343b3a39', '20db650a9c8e9a84ab4d25f7edc8f03f',
        'f8f9fafbfdfefe00020304050708090a0c0d0e0f11121314161718191b1c1d1e',
        'ecb-tbl-256: I=113'),
    ('a8a9aaab2221202fedecebea1e010003', '3c36da169525cf818843805f25b78ae5',
        '20212223252627282a2b2c2d2f30313234353637393a3b3c3e3f404143444546',
        'ecb-tbl-256: I=114'),
    ('f9f8fbfa5f5c5d42424344450e010003', '9a781d960db9e45e37779042fea51922',
        '48494a4b4d4e4f50525354555758595a5c5d5e5f61626364666768696b6c6d6e',
        'ecb-tbl-256: I=115'),
    ('57565554f5f6f7f89697909120dfdedd', '6560395ec269c672a3c288226efdba77',
        '70717273757677787a7b7c7d7f80818284858687898a8b8c8e8f909193949596',
        'ecb-tbl-256: I=116'),
    ('f8f9fafbcccfcef1dddcdbda0e010003', '8c772b7a189ac544453d5916ebb27b9a',
        '98999a9b9d9e9fa0a2a3a4a5a7a8a9aaacadaeafb1b2b3b4b6b7b8b9bbbcbdbe',
        'ecb-tbl-256: I=117'),
    ('d9d8dbda7073727d80818687c2dddcdf', '77ca5468cc48e843d05f78eed9d6578f',
        'c0c1c2c3c5c6c7c8cacbcccdcfd0d1d2d4d5d6d7d9dadbdcdedfe0e1e3e4e5e6',
        'ecb-tbl-256: I=118'),
    ('c5c4c7c6080b0a1588898e8f68676665', '72cdcc71dc82c60d4429c9e2d8195baa',
        'e8e9eaebedeeeff0f2f3f4f5f7f8f9fafcfdfeff01020304060708090b0c0d0e',
        'ecb-tbl-256: I=119'),
    ('83828180dcdfded186878081f0cfcecd', '8080d68ce60e94b40b5b8b69eeb35afa',
        '10111213151617181a1b1c1d1f20212224252627292a2b2c2e2f303133343536',
        'ecb-tbl-256: I=120'),
    ('98999a9bdddedfa079787f7e0a050407', '44222d3cde299c04369d58ac0eba1e8e',
        '38393a3b3d3e3f40424344454748494a4c4d4e4f51525354565758595b5c5d5e',
        'ecb-tbl-256: I=121'),
    ('cecfcccd4f4c4d429f9e9998dfc0c1c2', '9b8721b0a8dfc691c5bc5885dbfcb27a',
        '60616263656667686a6b6c6d6f70717274757677797a7b7c7e7f808183848586',
        'ecb-tbl-256: I=122'),
    ('404142436665647b29282f2eaba4a5a6', '0dc015ce9a3a3414b5e62ec643384183',
        '88898a8b8d8e8f90929394959798999a9c9d9e9fa1a2a3a4a6a7a8a9abacadae',
        'ecb-tbl-256: I=123'),
    ('33323130e6e5e4eb23222524dea1a0a3', '705715448a8da412025ce38345c2a148',
        'b0b1b2b3b5b6b7b8babbbcbdbfc0c1c2c4c5c6c7c9cacbcccecfd0d1d3d4d5d6',
        'ecb-tbl-256: I=124'),
    ('cfcecdccf6f5f4cbe6e7e0e199969794', 'c32b5b0b6fbae165266c569f4b6ecf0b',
        'd8d9dadbdddedfe0e2e3e4e5e7e8e9eaecedeeeff1f2f3f4f6f7f8f9fbfcfdfe',
        'ecb-tbl-256: I=125'),
    ('babbb8b97271707fdcdddadb29363734', '4dca6c75192a01ddca9476af2a521e87',
        '00010203050607080a0b0c0d0f10111214151617191a1b1c1e1f202123242526',
        'ecb-tbl-256: I=126'),
    ('c9c8cbca4447465926272021545b5a59', '058691e627ecbc36ac07b6db423bd698',
        '28292a2b2d2e2f30323334353738393a3c3d3e3f41424344464748494b4c4d4e',
        'ecb-tbl-256: I=127'),
    ('050407067477767956575051221d1c1f', '7444527095838fe080fc2bcdd30847eb',
        '50515253555657585a5b5c5d5f60616264656667696a6b6c6e6f707173747576',
        'ecb-tbl-256: I=128'),

    # FIPS PUB 800-38A test vectors, 2001 edition. Annex F.

    ('6bc1bee22e409f96e93d7e117393172a'+'ae2d8a571e03ac9c9eb76fac45af8e51'+
     '30c81c46a35ce411e5fbc1191a0a52ef'+'f69f2445df4f9b17ad2b417be66c3710',
     '3ad77bb40d7a3660a89ecaf32466ef97'+'f5d3d58503b9699de785895a96fdbaaf'+
     '43b1cd7f598ece23881b00e3ed030688'+'7b0c785e27e8ad3f8223207104725dd4',
     '2b7e151628aed2a6abf7158809cf4f3c',
     'NIST 800-38A, F.1.1, ECB and AES-128'),

    ('6bc1bee22e409f96e93d7e117393172a'+'ae2d8a571e03ac9c9eb76fac45af8e51'+
     '30c81c46a35ce411e5fbc1191a0a52ef'+'f69f2445df4f9b17ad2b417be66c3710',
     'bd334f1d6e45f25ff712a214571fa5cc'+'974104846d0ad3ad7734ecb3ecee4eef'+
     'ef7afd2270e2e60adce0ba2face6444e'+'9a4b41ba738d6c72fb16691603c18e0e',
     '8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b',
     'NIST 800-38A, F.1.3, ECB and AES-192'),

    ('6bc1bee22e409f96e93d7e117393172a'+'ae2d8a571e03ac9c9eb76fac45af8e51'+
     '30c81c46a35ce411e5fbc1191a0a52ef'+'f69f2445df4f9b17ad2b417be66c3710',
     'f3eed1bdb5d2a03c064b5a7e3db181f8'+'591ccb10d410ed26dc5ba74a31362870'+
     'b6ed21b99ca6f4f9f153e7b1beafed1d'+'23304b7a39f9f3ff067d8d8f9e24ecc7',
     '603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4',
     'NIST 800-38A, F.1.3, ECB and AES-256'),

    ('6bc1bee22e409f96e93d7e117393172a'+'ae2d8a571e03ac9c9eb76fac45af8e51'+
     '30c81c46a35ce411e5fbc1191a0a52ef'+'f69f2445df4f9b17ad2b417be66c3710',
     '7649abac8119b246cee98e9b12e9197d'+'5086cb9b507219ee95db113a917678b2'+
     '73bed6b8e3c1743b7116e69e22229516'+'3ff1caa1681fac09120eca307586e1a7',
     '2b7e151628aed2a6abf7158809cf4f3c',
     'NIST 800-38A, F.2.1, CBC and AES-128',
     dict(mode='CBC', iv='000102030405060708090a0b0c0d0e0f')),

    ('6bc1bee22e409f96e93d7e117393172a'+'ae2d8a571e03ac9c9eb76fac45af8e51'+
     '30c81c46a35ce411e5fbc1191a0a52ef'+'f69f2445df4f9b17ad2b417be66c3710',
     '4f021db243bc633d7178183a9fa071e8'+'b4d9ada9ad7dedf4e5e738763f69145a'+
     '571b242012fb7ae07fa9baac3df102e0'+'08b0e27988598881d920a9e64f5615cd',
     '8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b',
     'NIST 800-38A, F.2.1, CBC and AES-192',
     dict(mode='CBC', iv='000102030405060708090a0b0c0d0e0f')),

    ('6bc1bee22e409f96e93d7e117393172a'+'ae2d8a571e03ac9c9eb76fac45af8e51'+
     '30c81c46a35ce411e5fbc1191a0a52ef'+'f69f2445df4f9b17ad2b417be66c3710',
     'f58c4c04d6e5f1ba779eabfb5f7bfbd6'+'9cfc4e967edb808d679f777bc6702c7d'+
     '39f23369a9d9bacfa530e26304231461'+'b2eb05e2c39be9fcda6c19078c6a9d1b',
     '603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4',
     'NIST 800-38A, F.2.1, CBC and AES-256',
     dict(mode='CBC', iv='000102030405060708090a0b0c0d0e0f')),

    # Skip CFB-1 since it is not supported by PyCrypto

    ('6bc1bee22e409f96e93d7e117393172aae2d','3b79424c9c0dd436bace9e0ed4586a4f32b9',
     '2b7e151628aed2a6abf7158809cf4f3c',
     'NIST 800-38A, F.3.7, CFB-8 and AES-128',
     dict(mode='CFB', iv='000102030405060708090a0b0c0d0e0f', segment_size=8)),

    ('6bc1bee22e409f96e93d7e117393172aae2d','cda2521ef0a905ca44cd057cbf0d47a0678a',
     '8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b',
     'NIST 800-38A, F.3.9, CFB-8 and AES-192',
     dict(mode='CFB', iv='000102030405060708090a0b0c0d0e0f', segment_size=8)),

    ('6bc1bee22e409f96e93d7e117393172aae2d','dc1f1a8520a64db55fcc8ac554844e889700',
     '603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4',
     'NIST 800-38A, F.3.11, CFB-8 and AES-256',
     dict(mode='CFB', iv='000102030405060708090a0b0c0d0e0f', segment_size=8)),

    ('6bc1bee22e409f96e93d7e117393172a'+'ae2d8a571e03ac9c9eb76fac45af8e51'+
     '30c81c46a35ce411e5fbc1191a0a52ef'+'f69f2445df4f9b17ad2b417be66c3710',
     '3b3fd92eb72dad20333449f8e83cfb4a'+'c8a64537a0b3a93fcde3cdad9f1ce58b'+
     '26751f67a3cbb140b1808cf187a4f4df'+'c04b05357c5d1c0eeac4c66f9ff7f2e6',
     '2b7e151628aed2a6abf7158809cf4f3c',
     'NIST 800-38A, F.3.13, CFB-128 and AES-128',
     dict(mode='CFB', iv='000102030405060708090a0b0c0d0e0f', segment_size=128)),

    ('6bc1bee22e409f96e93d7e117393172a'+'ae2d8a571e03ac9c9eb76fac45af8e51'+
     '30c81c46a35ce411e5fbc1191a0a52ef'+'f69f2445df4f9b17ad2b417be66c3710',
     'cdc80d6fddf18cab34c25909c99a4174'+'67ce7f7f81173621961a2b70171d3d7a'+
     '2e1e8a1dd59b88b1c8e60fed1efac4c9'+'c05f9f9ca9834fa042ae8fba584b09ff',
     '8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b',
     'NIST 800-38A, F.3.15, CFB-128 and AES-192',
     dict(mode='CFB', iv='000102030405060708090a0b0c0d0e0f', segment_size=128)),

    ('6bc1bee22e409f96e93d7e117393172a'+'ae2d8a571e03ac9c9eb76fac45af8e51'+
     '30c81c46a35ce411e5fbc1191a0a52ef'+'f69f2445df4f9b17ad2b417be66c3710',
     'dc7e84bfda79164b7ecd8486985d3860'+'39ffed143b28b1c832113c6331e5407b'+
     'df10132415e54b92a13ed0a8267ae2f9'+'75a385741ab9cef82031623d55b1e471',
     '603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4',
     'NIST 800-38A, F.3.17, CFB-128 and AES-256',
     dict(mode='CFB', iv='000102030405060708090a0b0c0d0e0f', segment_size=128)),

    ('6bc1bee22e409f96e93d7e117393172a'+'ae2d8a571e03ac9c9eb76fac45af8e51'+
     '30c81c46a35ce411e5fbc1191a0a52ef'+'f69f2445df4f9b17ad2b417be66c3710',
     '3b3fd92eb72dad20333449f8e83cfb4a'+'7789508d16918f03f53c52dac54ed825'+
     '9740051e9c5fecf64344f7a82260edcc'+'304c6528f659c77866a510d9c1d6ae5e',
     '2b7e151628aed2a6abf7158809cf4f3c',
     'NIST 800-38A, F.4.1, OFB and AES-128',
     dict(mode='OFB', iv='000102030405060708090a0b0c0d0e0f')),

    ('6bc1bee22e409f96e93d7e117393172a'+'ae2d8a571e03ac9c9eb76fac45af8e51'+
     '30c81c46a35ce411e5fbc1191a0a52ef'+'f69f2445df4f9b17ad2b417be66c3710',
     'cdc80d6fddf18cab34c25909c99a4174'+'fcc28b8d4c63837c09e81700c1100401'+
     '8d9a9aeac0f6596f559c6d4daf59a5f2'+'6d9f200857ca6c3e9cac524bd9acc92a',
     '8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b',
     'NIST 800-38A, F.4.3, OFB and AES-192',
     dict(mode='OFB', iv='000102030405060708090a0b0c0d0e0f')),

    ('6bc1bee22e409f96e93d7e117393172a'+'ae2d8a571e03ac9c9eb76fac45af8e51'+
     '30c81c46a35ce411e5fbc1191a0a52ef'+'f69f2445df4f9b17ad2b417be66c3710',
     'dc7e84bfda79164b7ecd8486985d3860'+'4febdc6740d20b3ac88f6ad82a4fb08d'+
     '71ab47a086e86eedf39d1c5bba97c408'+'0126141d67f37be8538f5a8be740e484',
     '603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4',
     'NIST 800-38A, F.4.5, OFB and AES-256',
     dict(mode='OFB', iv='000102030405060708090a0b0c0d0e0f')),

    ('6bc1bee22e409f96e93d7e117393172a'+'ae2d8a571e03ac9c9eb76fac45af8e51'+
     '30c81c46a35ce411e5fbc1191a0a52ef'+'f69f2445df4f9b17',
     '3b3fd92eb72dad20333449f8e83cfb4a'+'7789508d16918f03f53c52dac54ed825'+
     '9740051e9c5fecf64344f7a82260edcc'+'304c6528f659c778',
     '2b7e151628aed2a6abf7158809cf4f3c',
     'NIST 800-38A, F.4.1, OFB and AES-128 (partial last block)',
     dict(mode='OFB', iv='000102030405060708090a0b0c0d0e0f')),

    ('6bc1bee22e409f96e93d7e117393172a'+'ae2d8a571e03ac9c9eb76fac45af8e51'+
     '30c81c46a35ce411e5fbc1191a0a52ef'+'f69f2445df4f9b17',
     'cdc80d6fddf18cab34c25909c99a4174'+'fcc28b8d4c63837c09e81700c1100401'+
     '8d9a9aeac0f6596f559c6d4daf59a5f2'+'6d9f200857ca6c3e',
     '8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b',
     'NIST 800-38A, F.4.3, OFB and AES-192 (partial last block)',
     dict(mode='OFB', iv='000102030405060708090a0b0c0d0e0f')),

    ('6bc1bee22e409f96e93d7e117393172a'+'ae2d8a571e03ac9c9eb76fac45af8e51'+
     '30c81c46a35ce411e5fbc1191a0a52ef'+'f69f2445df4f9b17',
     'dc7e84bfda79164b7ecd8486985d3860'+'4febdc6740d20b3ac88f6ad82a4fb08d'+
     '71ab47a086e86eedf39d1c5bba97c408'+'0126141d67f37be8',
     '603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4',
     'NIST 800-38A, F.4.5, OFB and AES-256 (partial last block)',
     dict(mode='OFB', iv='000102030405060708090a0b0c0d0e0f')),

    ('6bc1bee22e409f96e93d7e117393172a'+'ae2d8a571e03ac9c9eb76fac45af8e51'+
     '30c81c46a35ce411e5fbc1191a0a52ef'+'f69f2445df4f9b17ad2b417be66c3710',
     '874d6191b620e3261bef6864990db6ce'+'9806f66b7970fdff8617187bb9fffdff'+
     '5ae4df3edbd5d35e5b4f09020db03eab'+'1e031dda2fbe03d1792170a0f3009cee',
     '2b7e151628aed2a6abf7158809cf4f3c',
     'NIST 800-38A, F.5.1, CTR and AES-128',
     dict(mode='CTR', ctr_params=dict(nbits=16, prefix='f0f1f2f3f4f5f6f7f8f9fafbfcfd', initial_value=0xfeff))),

    ('6bc1bee22e409f96e93d7e117393172a'+'ae2d8a571e03ac9c9eb76fac45af8e51'+
     '30c81c46a35ce411e5fbc1191a0a52ef'+'f69f2445df4f9b17ad2b417be66c3710',
     '1abc932417521ca24f2b0459fe7e6e0b'+'090339ec0aa6faefd5ccc2c6f4ce8e94'+
     '1e36b26bd1ebc670d1bd1d665620abf7'+'4f78a7f6d29809585a97daec58c6b050',
     '8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b',
     'NIST 800-38A, F.5.3, CTR and AES-192',
     dict(mode='CTR', ctr_params=dict(nbits=16, prefix='f0f1f2f3f4f5f6f7f8f9fafbfcfd', initial_value=0xfeff))),

    ('6bc1bee22e409f96e93d7e117393172a'+'ae2d8a571e03ac9c9eb76fac45af8e51'+
     '30c81c46a35ce411e5fbc1191a0a52ef'+'f69f2445df4f9b17ad2b417be66c3710',
     '601ec313775789a5b7a7f504bbf3d228'+'f443e3ca4d62b59aca84e990cacaf5c5'+
     '2b0930daa23de94ce87017ba2d84988d'+'dfc9c58db67aada613c2dd08457941a6',
     '603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4',
     'NIST 800-38A, F.5.5, CTR and AES-256',
     dict(mode='CTR', ctr_params=dict(nbits=16, prefix='f0f1f2f3f4f5f6f7f8f9fafbfcfd', initial_value=0xfeff))),

    # RFC 3686 test vectors
    # This is a list of (plaintext, ciphertext, key[, description[, params]]) tuples.
    ('53696e676c6520626c6f636b206d7367', 'e4095d4fb7a7b3792d6175a3261311b8',
        'ae6852f8121067cc4bf7a5765577f39e',
        'RFC 3686 Test Vector #1: Encrypting 16 octets using AES-CTR with 128-bit key',
        dict(mode='CTR', ctr_params=dict(nbits=32, prefix='00000030'+'0000000000000000'))),
    ('000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f',
        '5104a106168a72d9790d41ee8edad388eb2e1efc46da57c8fce630df9141be28',
        '7e24067817fae0d743d6ce1f32539163',
        'RFC 3686 Test Vector #2: Encrypting 32 octets using AES-CTR with 128-bit key',
        dict(mode='CTR', ctr_params=dict(nbits=32, prefix='006cb6db'+'c0543b59da48d90b'))),
    ('000102030405060708090a0b0c0d0e0f'+'101112131415161718191a1b1c1d1e1f'+'20212223',
        'c1cf48a89f2ffdd9cf4652e9efdb72d7'+'4540a42bde6d7836d59a5ceaaef31053'+'25b2072f',
        '7691be035e5020a8ac6e618529f9a0dc',
        'RFC 3686 Test Vector #3: Encrypting 36 octets using AES-CTR with 128-bit key',
        dict(mode='CTR', ctr_params=dict(nbits=32, prefix='00e0017b'+'27777f3f4a1786f0'))),
    ('53696e676c6520626c6f636b206d7367',
        '4b55384fe259c9c84e7935a003cbe928',
        '16af5b145fc9f579c175f93e3bfb0eed'+'863d06ccfdb78515',
        'RFC 3686 Test Vector #4: Encrypting 16 octets using AES-CTR with 192-bit key',
        dict(mode='CTR', ctr_params=dict(nbits=32, prefix='00000048'+'36733c147d6d93cb'))),
    ('000102030405060708090a0b0c0d0e0f'+'101112131415161718191a1b1c1d1e1f',
        '453243fc609b23327edfaafa7131cd9f'+'8490701c5ad4a79cfc1fe0ff42f4fb00',
        '7c5cb2401b3dc33c19e7340819e0f69c'+'678c3db8e6f6a91a',
        'RFC 3686 Test Vector #5: Encrypting 32 octets using AES-CTR with 192-bit key',
        dict(mode='CTR', ctr_params=dict(nbits=32, prefix='0096b03b'+'020c6eadc2cb500d'))),
    ('000102030405060708090a0b0c0d0e0f'+'101112131415161718191a1b1c1d1e1f'+'20212223',
        '96893fc55e5c722f540b7dd1ddf7e758'+'d288bc95c69165884536c811662f2188'+'abee0935',
        '02bf391ee8ecb159b959617b0965279b'+'f59b60a786d3e0fe',
        'RFC 3686 Test Vector #6: Encrypting 36 octets using AES-CTR with 192-bit key',
        dict(mode='CTR', ctr_params=dict(nbits=32, prefix='0007bdfd'+'5cbd60278dcc0912'))),
    ('53696e676c6520626c6f636b206d7367',
        '145ad01dbf824ec7560863dc71e3e0c0',
        '776beff2851db06f4c8a0542c8696f6c'+'6a81af1eec96b4d37fc1d689e6c1c104',
        'RFC 3686 Test Vector #7: Encrypting 16 octets using AES-CTR with 256-bit key',
        dict(mode='CTR', ctr_params=dict(nbits=32, prefix='00000060'+'db5672c97aa8f0b2'))),
    ('000102030405060708090a0b0c0d0e0f'+'101112131415161718191a1b1c1d1e1f',
        'f05e231b3894612c49ee000b804eb2a9'+'b8306b508f839d6a5530831d9344af1c',
        'f6d66d6bd52d59bb0796365879eff886'+'c66dd51a5b6a99744b50590c87a23884',
        'RFC 3686 Test Vector #8: Encrypting 32 octets using AES-CTR with 256-bit key',
        dict(mode='CTR', ctr_params=dict(nbits=32, prefix='00faac24'+'c1585ef15a43d875'))),
    ('000102030405060708090a0b0c0d0e0f'+'101112131415161718191a1b1c1d1e1f'+'20212223',
        'eb6c52821d0bbbf7ce7594462aca4faa'+'b407df866569fd07f48cc0b583d6071f'+'1ec0e6b8',
        'ff7a617ce69148e4f1726e2f43581de2'+'aa62d9f805532edff1eed687fb54153d',
        'RFC 3686 Test Vector #9: Encrypting 36 octets using AES-CTR with 256-bit key',
        dict(mode='CTR', ctr_params=dict(nbits=32, prefix='001cc5b7'+'51a51d70a1c11148'))),

    # The following test vectors have been generated with gpg v1.4.0.
    # The command line used was:
    #
    #    gpg -c -z 0 --cipher-algo AES --passphrase secret_passphrase \
    #     --disable-mdc --s2k-mode 0 --output ct pt
    #
    # As result, the content of the file 'pt' is encrypted with a key derived
    # from 'secret_passphrase' and written to file 'ct'.
    # Test vectors must be extracted from 'ct', which is a collection of
    # TLVs (see RFC4880 for all details):
    # - the encrypted data (with the encrypted IV as prefix) is the payload
    #   of the TLV with tag 9 (Symmetrical Encrypted Data Packet).
    #   This is the ciphertext in the test vector.
    # - inside the encrypted part, there is a further layer of TLVs. One must
    #   look for tag 11 (Literal Data  Packet); in its payload, after a short
    #   but time dependent header, there is the content of file 'pt'.
    #   In the test vector, the plaintext is the complete set of TLVs that gets
    #   encrypted. It is not just the content of 'pt'.
    # - the key is the leftmost 16 bytes of the SHA1 digest of the password.
    #   The test vector contains such shortened digest.
    #
    # Note that encryption uses a clear IV, and decryption an encrypted IV
    ( 'ac18620270744fb4f647426c61636b4361745768697465436174',   # Plaintext, 'BlackCatWhiteCat'
      'dc6b9e1f095de609765c59983db5956ae4f63aea7405389d2ebb',   # Ciphertext
      '5baa61e4c9b93f3f0682250b6cf8331b', # Key (hash of 'password')
      'GPG Test Vector #1',
      dict(mode='OPENPGP', iv='3d7d3e62282add7eb203eeba5c800733', encrypted_iv='fd934601ef49cb58b6d9aebca6056bdb96ef' ) ),

    # NIST SP 800-38C test vectors for CCM
    # This is a list of tuples with 5 items:
    #
    #  1. Associated data + '|' + plaintext
    #  2. Associated data + '|' + ciphertext + '|' + MAC
    #  3. AES-128 key
    #  4. Description
    #  5. Dictionary of parameters to be passed to AES.new().
    #     It must include the nonce.
    #
    ( '0001020304050607|20212223',
      '0001020304050607|7162015b|4dac255d',
      '404142434445464748494a4b4c4d4e4f',
      'NIST SP 800-38C Appex C.1',
      dict(mode='CCM', nonce='10111213141516')
    ),
    ( '000102030405060708090a0b0c0d0e0f|202122232425262728292a2b2c2d2e2f',
      '000102030405060708090a0b0c0d0e0f|d2a1f0e051ea5f62081a7792073d593d|1fc64fbfaccd',
      '404142434445464748494a4b4c4d4e4f',
      'NIST SP 800-38C Appex C.2',
      dict(mode='CCM', nonce='1011121314151617')
    ),
    ( '000102030405060708090a0b0c0d0e0f10111213|'+
      '202122232425262728292a2b2c2d2e2f3031323334353637',
      '000102030405060708090a0b0c0d0e0f10111213|'+
      'e3b201a9f5b71a7a9b1ceaeccd97e70b6176aad9a4428aa5|484392fbc1b09951',
      '404142434445464748494a4b4c4d4e4f',
      'NIST SP 800-38C Appex C.3',
      dict(mode='CCM', nonce='101112131415161718191a1b')
    ),
    (
      (''.join(["%02X" % (x*16+y) for x in xrange(0,16) for y in xrange(0,16)]))*256+'|'+
      '202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f',
      (''.join(["%02X" % (x*16+y) for x in xrange(0,16) for y in xrange(0,16)]))*256+'|'+
      '69915dad1e84c6376a68c2967e4dab615ae0fd1faec44cc484828529463ccf72|'+
      'b4ac6bec93e8598e7f0dadbcea5b',
      '404142434445464748494a4b4c4d4e4f',
      'NIST SP 800-38C Appex C.4',
      dict(mode='CCM', nonce='101112131415161718191a1b1c')
    ),
    # RFC3610 test vectors
    (
      '0001020304050607|08090a0b0c0d0e0f101112131415161718191a1b1c1d1e',
      '0001020304050607|588c979a61c663d2f066d0c2c0f989806d5f6b61dac384|'+
      '17e8d12cfdf926e0',
      'c0c1c2c3c4c5c6c7c8c9cacbcccdcecf',
      'RFC3610 Packet Vector #1',
      dict(mode='CCM', nonce='00000003020100a0a1a2a3a4a5')
    ),
    (
      '0001020304050607|08090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f',
      '0001020304050607|72c91a36e135f8cf291ca894085c87e3cc15c439c9e43a3b|'+
      'a091d56e10400916',
      'c0c1c2c3c4c5c6c7c8c9cacbcccdcecf',
      'RFC3610 Packet Vector #2',
      dict(mode='CCM', nonce='00000004030201a0a1a2a3a4a5')
    ),
    (
      '0001020304050607|08090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f20',
      '0001020304050607|51b1e5f44a197d1da46b0f8e2d282ae871e838bb64da859657|'+
      '4adaa76fbd9fb0c5',
      'c0c1c2c3c4c5c6c7c8c9cacbcccdcecf',
      'RFC3610 Packet Vector #3',
      dict(mode='CCM', nonce='00000005040302A0A1A2A3A4A5')
    ),
    (
      '000102030405060708090a0b|0c0d0e0f101112131415161718191a1b1c1d1e',
      '000102030405060708090a0b|a28c6865939a9a79faaa5c4c2a9d4a91cdac8c|'+
      '96c861b9c9e61ef1',
      'c0c1c2c3c4c5c6c7c8c9cacbcccdcecf',
      'RFC3610 Packet Vector #4',
      dict(mode='CCM', nonce='00000006050403a0a1a2a3a4a5')
    ),
    (
      '000102030405060708090a0b|0c0d0e0f101112131415161718191a1b1c1d1e1f',
      '000102030405060708090a0b|dcf1fb7b5d9e23fb9d4e131253658ad86ebdca3e|'+
      '51e83f077d9c2d93',
      'c0c1c2c3c4c5c6c7c8c9cacbcccdcecf',
      'RFC3610 Packet Vector #5',
      dict(mode='CCM', nonce='00000007060504a0a1a2a3a4a5')
    ),
    (
      '000102030405060708090a0b|0c0d0e0f101112131415161718191a1b1c1d1e1f20',
      '000102030405060708090a0b|6fc1b011f006568b5171a42d953d469b2570a4bd87|'+
      '405a0443ac91cb94',
      'c0c1c2c3c4c5c6c7c8c9cacbcccdcecf',
      'RFC3610 Packet Vector #6',
      dict(mode='CCM', nonce='00000008070605a0a1a2a3a4a5')
    ),
    (
      '0001020304050607|08090a0b0c0d0e0f101112131415161718191a1b1c1d1e',
      '0001020304050607|0135d1b2c95f41d5d1d4fec185d166b8094e999dfed96c|'+
      '048c56602c97acbb7490',
      'c0c1c2c3c4c5c6c7c8c9cacbcccdcecf',
      'RFC3610 Packet Vector #7',
      dict(mode='CCM', nonce='00000009080706a0a1a2a3a4a5')
    ),
    (
      '0001020304050607|08090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f',
      '0001020304050607|7b75399ac0831dd2f0bbd75879a2fd8f6cae6b6cd9b7db24|'+
      'c17b4433f434963f34b4',
      'c0c1c2c3c4c5c6c7c8c9cacbcccdcecf',
      'RFC3610 Packet Vector #8',
      dict(mode='CCM', nonce='0000000a090807a0a1a2a3a4a5')
    ),
    (
      '0001020304050607|08090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f20',
      '0001020304050607|82531a60cc24945a4b8279181ab5c84df21ce7f9b73f42e197|'+
      'ea9c07e56b5eb17e5f4e',
      'c0c1c2c3c4c5c6c7c8c9cacbcccdcecf',
      'RFC3610 Packet Vector #9',
      dict(mode='CCM', nonce='0000000b0a0908a0a1a2a3a4a5')
    ),
    (
      '000102030405060708090a0b|0c0d0e0f101112131415161718191a1b1c1d1e',
      '000102030405060708090a0b|07342594157785152b074098330abb141b947b|'+
      '566aa9406b4d999988dd',
      'c0c1c2c3c4c5c6c7c8c9cacbcccdcecf',
      'RFC3610 Packet Vector #10',
      dict(mode='CCM', nonce='0000000c0b0a09a0a1a2a3a4a5')
    ),
    (
      '000102030405060708090a0b|0c0d0e0f101112131415161718191a1b1c1d1e1f',
      '000102030405060708090a0b|676bb20380b0e301e8ab79590a396da78b834934|'+
      'f53aa2e9107a8b6c022c',
      'c0c1c2c3c4c5c6c7c8c9cacbcccdcecf',
      'RFC3610 Packet Vector #11',
      dict(mode='CCM', nonce='0000000d0c0b0aa0a1a2a3a4a5')
    ),
    (
      '000102030405060708090a0b|0c0d0e0f101112131415161718191a1b1c1d1e1f20',
      '000102030405060708090a0b|c0ffa0d6f05bdb67f24d43a4338d2aa4bed7b20e43|'+
      'cd1aa31662e7ad65d6db',
      'c0c1c2c3c4c5c6c7c8c9cacbcccdcecf',
      'RFC3610 Packet Vector #12',
      dict(mode='CCM', nonce='0000000e0d0c0ba0a1a2a3a4a5')
    ),
    (
      '0be1a88bace018b1|08e8cf97d820ea258460e96ad9cf5289054d895ceac47c',
      '0be1a88bace018b1|4cb97f86a2a4689a877947ab8091ef5386a6ffbdd080f8|'+
      'e78cf7cb0cddd7b3',
      'd7828d13b2b0bdc325a76236df93cc6b',
      'RFC3610 Packet Vector #13',
      dict(mode='CCM', nonce='00412b4ea9cdbe3c9696766cfa')
    ),
    (
      '63018f76dc8a1bcb|9020ea6f91bdd85afa0039ba4baff9bfb79c7028949cd0ec',
      '63018f76dc8a1bcb|4ccb1e7ca981befaa0726c55d378061298c85c92814abc33|'+
      'c52ee81d7d77c08a',
      'd7828d13b2b0bdc325a76236df93cc6b',
      'RFC3610 Packet Vector #14',
      dict(mode='CCM', nonce='0033568ef7b2633c9696766cfa')
    ),
    (
      'aa6cfa36cae86b40|b916e0eacc1c00d7dcec68ec0b3bbb1a02de8a2d1aa346132e',
      'aa6cfa36cae86b40|b1d23a2220ddc0ac900d9aa03c61fcf4a559a4417767089708|'+
      'a776796edb723506',
      'd7828d13b2b0bdc325a76236df93cc6b',
      'RFC3610 Packet Vector #15',
      dict(mode='CCM', nonce='00103fe41336713c9696766cfa')
    ),
    (
      'd0d0735c531e1becf049c244|12daac5630efa5396f770ce1a66b21f7b2101c',
      'd0d0735c531e1becf049c244|14d253c3967b70609b7cbb7c49916028324526|'+
      '9a6f49975bcadeaf',
      'd7828d13b2b0bdc325a76236df93cc6b',
      'RFC3610 Packet Vector #16',
      dict(mode='CCM', nonce='00764c63b8058e3c9696766cfa')
    ),
    (
      '77b60f011c03e1525899bcae|e88b6a46c78d63e52eb8c546efb5de6f75e9cc0d',
      '77b60f011c03e1525899bcae|5545ff1a085ee2efbf52b2e04bee1e2336c73e3f|'+
      '762c0c7744fe7e3c',
      'd7828d13b2b0bdc325a76236df93cc6b',
      'RFC3610 Packet Vector #17',
      dict(mode='CCM', nonce='00f8b678094e3b3c9696766cfa')
    ),
    (
      'cd9044d2b71fdb8120ea60c0|6435acbafb11a82e2f071d7ca4a5ebd93a803ba87f',
      'cd9044d2b71fdb8120ea60c0|009769ecabdf48625594c59251e6035722675e04c8|'+
      '47099e5ae0704551',
      'd7828d13b2b0bdc325a76236df93cc6b',
      'RFC3610 Packet Vector #18',
      dict(mode='CCM', nonce='00d560912d3f703c9696766cfa')
    ),
    (
      'd85bc7e69f944fb8|8a19b950bcf71a018e5e6701c91787659809d67dbedd18',
      'd85bc7e69f944fb8|bc218daa947427b6db386a99ac1aef23ade0b52939cb6a|'+
      '637cf9bec2408897c6ba',
      'd7828d13b2b0bdc325a76236df93cc6b',
      'RFC3610 Packet Vector #19',
      dict(mode='CCM', nonce='0042fff8f1951c3c9696766cfa')
    ),
    (
      '74a0ebc9069f5b37|1761433c37c5a35fc1f39f406302eb907c6163be38c98437',
      '74a0ebc9069f5b37|5810e6fd25874022e80361a478e3e9cf484ab04f447efff6|'+
      'f0a477cc2fc9bf548944',
      'd7828d13b2b0bdc325a76236df93cc6b',
      'RFC3610 Packet Vector #20',
      dict(mode='CCM', nonce='00920f40e56cdc3c9696766cfa')
    ),
    (
      '44a3aa3aae6475ca|a434a8e58500c6e41530538862d686ea9e81301b5ae4226bfa',
      '44a3aa3aae6475ca|f2beed7bc5098e83feb5b31608f8e29c38819a89c8e776f154|'+
      '4d4151a4ed3a8b87b9ce',
      'd7828d13b2b0bdc325a76236df93cc6b',
      'RFC3610 Packet Vector #21',
      dict(mode='CCM', nonce='0027ca0c7120bc3c9696766cfa')
    ),
    (
      'ec46bb63b02520c33c49fd70|b96b49e21d621741632875db7f6c9243d2d7c2',
      'ec46bb63b02520c33c49fd70|31d750a09da3ed7fddd49a2032aabf17ec8ebf|'+
      '7d22c8088c666be5c197',
      'd7828d13b2b0bdc325a76236df93cc6b',
      'RFC3610 Packet Vector #22',
      dict(mode='CCM', nonce='005b8ccbcd9af83c9696766cfa')
    ),
    (
      '47a65ac78b3d594227e85e71|e2fcfbb880442c731bf95167c8ffd7895e337076',
      '47a65ac78b3d594227e85e71|e882f1dbd38ce3eda7c23f04dd65071eb41342ac|'+
      'df7e00dccec7ae52987d',
      'd7828d13b2b0bdc325a76236df93cc6b',
      'RFC3610 Packet Vector #23',
      dict(mode='CCM', nonce='003ebe94044b9a3c9696766cfa')
    ),
    (
      '6e37a6ef546d955d34ab6059|abf21c0b02feb88f856df4a37381bce3cc128517d4',
      '6e37a6ef546d955d34ab6059|f32905b88a641b04b9c9ffb58cc390900f3da12ab1|'+
      '6dce9e82efa16da62059',
      'd7828d13b2b0bdc325a76236df93cc6b',
      'RFC3610 Packet Vector #24',
      dict(mode='CCM', nonce='008d493b30ae8b3c9696766cfa')
    ),

    # Test vectors for EAX taken from http://www.cs.ucdavis.edu/~rogaway/papers/eax.pdf
    # This is a list of tuples with 5 items:
    #
    #  1. Header + '|' + plaintext
    #  2. Header + '|' + ciphertext + '|' + MAC
    #  3. AES-128 key
    #  4. Description
    #  5. Dictionary of parameters to be passed to AES.new(). It must
    #     include the nonce.
    #
    ( '6bfb914fd07eae6b|',
      '6bfb914fd07eae6b||e037830e8389f27b025a2d6527e79d01',
      '233952dee4d5ed5f9b9c6d6ff80ff478',
      'EAX spec Appendix G',
      dict(mode='EAX', nonce='62EC67F9C3A4A407FCB2A8C49031A8B3')
    ),

    ( 'fa3bfd4806eb53fa|f7fb',
      'fa3bfd4806eb53fa|19dd|5c4c9331049d0bdab0277408f67967e5',
      '91945d3f4dcbee0bf45ef52255f095a4',
      'EAX spec Appendix G',
      dict(mode='EAX', nonce='BECAF043B0A23D843194BA972C66DEBD')
    ),

    ( '234a3463c1264ac6|1a47cb4933',
      '234a3463c1264ac6|d851d5bae0|3a59f238a23e39199dc9266626c40f80',
      '01f74ad64077f2e704c0f60ada3dd523',
      'EAX spec Appendix G',
      dict(mode='EAX', nonce='70C3DB4F0D26368400A10ED05D2BFF5E')
    ),

    ( '33cce2eabff5a79d|481c9e39b1',
      '33cce2eabff5a79d|632a9d131a|d4c168a4225d8e1ff755939974a7bede',
      'd07cf6cbb7f313bdde66b727afd3c5e8',
      'EAX spec Appendix G',
      dict(mode='EAX', nonce='8408DFFF3C1A2B1292DC199E46B7D617')
    ),

    ( 'aeb96eaebe2970e9|40d0c07da5e4',
      'aeb96eaebe2970e9|071dfe16c675|cb0677e536f73afe6a14b74ee49844dd',
      '35b6d0580005bbc12b0587124557d2c2',
      'EAX spec Appendix G',
      dict(mode='EAX', nonce='FDB6B06676EEDC5C61D74276E1F8E816')
    ),

    ( 'd4482d1ca78dce0f|4de3b35c3fc039245bd1fb7d',
      'd4482d1ca78dce0f|835bb4f15d743e350e728414|abb8644fd6ccb86947c5e10590210a4f',
      'bd8e6e11475e60b268784c38c62feb22',
      'EAX spec Appendix G',
      dict(mode='EAX', nonce='6EAC5C93072D8E8513F750935E46DA1B')
    ),

    ( '65d2017990d62528|8b0a79306c9ce7ed99dae4f87f8dd61636',
      '65d2017990d62528|02083e3979da014812f59f11d52630da30|137327d10649b0aa6e1c181db617d7f2',
      '7c77d6e813bed5ac98baa417477a2e7d',
      'EAX spec Appendix G',
      dict(mode='EAX', nonce='1A8C98DCD73D38393B2BF1569DEEFC19')
    ),

    ( '54b9f04e6a09189a|1bda122bce8a8dbaf1877d962b8592dd2d56',
      '54b9f04e6a09189a|2ec47b2c4954a489afc7ba4897edcdae8cc3|3b60450599bd02c96382902aef7f832a',
      '5fff20cafab119ca2fc73549e20f5b0d',
      'EAX spec Appendix G',
      dict(mode='EAX', nonce='DDE59B97D722156D4D9AFF2BC7559826')
    ),

    ( '899a175897561d7e|6cf36720872b8513f6eab1a8a44438d5ef11',
      '899a175897561d7e|0de18fd0fdd91e7af19f1d8ee8733938b1e8|e7f6d2231618102fdb7fe55ff1991700',
      'a4a4782bcffd3ec5e7ef6d8c34a56123',
      'EAX spec Appendix G',
      dict(mode='EAX', nonce='B781FCF2F75FA5A8DE97A9CA48E522EC')
    ),

    ( '126735fcc320d25a|ca40d7446e545ffaed3bd12a740a659ffbbb3ceab7',
      '126735fcc320d25a|cb8920f87a6c75cff39627b56e3ed197c552d295a7|cfc46afc253b4652b1af3795b124ab6e',
      '8395fcf1e95bebd697bd010bc766aac3',
      'EAX spec Appendix G',
      dict(mode='EAX', nonce='22E7ADD93CFC6393C57EC0B3C17D6B44')
    ),

    # Test vectors for SIV taken from RFC5297
    # This is a list of tuples with 5 items:
    #
    #  1. Header + '|' + plaintext
    #  2. Header + '|' + ciphertext + '|' + MAC
    #  3. AES-128 key
    #  4. Description
    #  5. Dictionary of parameters to be passed to AES.new().
    #     It must include the nonce.
    #
    #  A "Header" is a dash ('-') separated sequece of components.
    #
    ( '101112131415161718191a1b1c1d1e1f2021222324252627|112233445566778899aabbccddee',
      '101112131415161718191a1b1c1d1e1f2021222324252627|40c02b9690c4dc04daef7f6afe5c|' +
      '85632d07c6e8f37f950acd320a2ecc93',
      'fffefdfcfbfaf9f8f7f6f5f4f3f2f1f0f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff',
      'RFC5297 A.1',
      dict(mode='SIV', nonce=None)
    ),

    ( '00112233445566778899aabbccddeeffdeaddadadeaddadaffeeddccbbaa9988' +
      '7766554433221100-102030405060708090a0|' +
      '7468697320697320736f6d6520706c61696e7465787420746f20656e63727970' +
      '74207573696e67205349562d414553',

      '00112233445566778899aabbccddeeffdeaddadadeaddadaffeeddccbbaa9988' +
      '7766554433221100-102030405060708090a0|' +
      'cb900f2fddbe404326601965c889bf17dba77ceb094fa663b7a3f748ba8af829' +
      'ea64ad544a272e9c485b62a3fd5c0d|' +
      '7bdb6e3b432667eb06f4d14bff2fbd0f',

      '7f7e7d7c7b7a79787776757473727170404142434445464748494a4b4c4d4e4f',
      'RFC5297 A.2',
      dict(mode='SIV', nonce='09f911029d74e35bd84156c5635688c0')
    ),

    # Test vectors for GCM taken from
    # http://csrc.nist.gov/groups/ST/toolkit/BCM/documents/proposedmodes/gcm/gcm-revised-spec.pdf
    # This is a list of tuples with 5 items:
    #
    #  1. Header + '|' + plaintext
    #  2. Header + '|' + ciphertext + '|' + MAC
    #  3. AES-128 key
    #  4. Description
    #  5. Dictionary of parameters to be passed to AES.new().
    #     It must include the nonce.
    #
    ( '|',
      '||58e2fccefa7e3061367f1d57a4e7455a',
      '00000000000000000000000000000000',
      'GCM Test Case 1',
      dict(mode='GCM', nonce='000000000000000000000000')
    ),

    ( '|00000000000000000000000000000000',
      '|0388dace60b6a392f328c2b971b2fe78|ab6e47d42cec13bdf53a67b21257bddf',
      '00000000000000000000000000000000',
      'GCM Test Case 2',
      dict(mode='GCM', nonce='000000000000000000000000')
    ),

    ( '|d9313225f88406e5a55909c5aff5269a86a7a9531534f7da2e4c303d8a318a72' +
       '1c3c0c95956809532fcf0e2449a6b525b16aedf5aa0de657ba637b391aafd255',
      '|42831ec2217774244b7221b784d0d49ce3aa212f2c02a4e035c17e2329aca12e'  +
       '21d514b25466931c7d8f6a5aac84aa051ba30b396a0aac973d58e091473f5985|' +
       '4d5c2af327cd64a62cf35abd2ba6fab4',
      'feffe9928665731c6d6a8f9467308308',
      'GCM Test Case 3',
      dict(mode='GCM', nonce='cafebabefacedbaddecaf888')
    ),

    ( 'feedfacedeadbeeffeedfacedeadbeefabaddad2|' +
      'd9313225f88406e5a55909c5aff5269a86a7a9531534f7da2e4c303d8a318a72' +
      '1c3c0c95956809532fcf0e2449a6b525b16aedf5aa0de657ba637b39',
      'feedfacedeadbeeffeedfacedeadbeefabaddad2|' +
      '42831ec2217774244b7221b784d0d49ce3aa212f2c02a4e035c17e2329aca12e'  +
      '21d514b25466931c7d8f6a5aac84aa051ba30b396a0aac973d58e091|' +
      '5bc94fbc3221a5db94fae95ae7121a47',
      'feffe9928665731c6d6a8f9467308308',
      'GCM Test Case 4',
      dict(mode='GCM', nonce='cafebabefacedbaddecaf888')
    ),

    ( 'feedfacedeadbeeffeedfacedeadbeefabaddad2|' +
      'd9313225f88406e5a55909c5aff5269a86a7a9531534f7da2e4c303d8a318a72' +
      '1c3c0c95956809532fcf0e2449a6b525b16aedf5aa0de657ba637b39',
      'feedfacedeadbeeffeedfacedeadbeefabaddad2|' +
      '61353b4c2806934a777ff51fa22a4755699b2a714fcdc6f83766e5f97b6c7423' +
      '73806900e49f24b22b097544d4896b424989b5e1ebac0f07c23f4598|' +
      '3612d2e79e3b0785561be14aaca2fccb',
      'feffe9928665731c6d6a8f9467308308',
      'GCM Test Case 5',
      dict(mode='GCM', nonce='cafebabefacedbad')
    ),

    ( 'feedfacedeadbeeffeedfacedeadbeefabaddad2|' +
      'd9313225f88406e5a55909c5aff5269a86a7a9531534f7da2e4c303d8a318a72' +
      '1c3c0c95956809532fcf0e2449a6b525b16aedf5aa0de657ba637b39',
      'feedfacedeadbeeffeedfacedeadbeefabaddad2|' +
      '8ce24998625615b603a033aca13fb894be9112a5c3a211a8ba262a3cca7e2ca7' +
      '01e4a9a4fba43c90ccdcb281d48c7c6fd62875d2aca417034c34aee5|' +
      '619cc5aefffe0bfa462af43c1699d050',
      'feffe9928665731c6d6a8f9467308308',
      'GCM Test Case 6',
      dict(mode='GCM', nonce='9313225df88406e555909c5aff5269aa'+
          '6a7a9538534f7da1e4c303d2a318a728c3c0c95156809539fcf0e2429a6b5254'+
          '16aedbf5a0de6a57a637b39b' )
    ),

    ( '|',
      '||cd33b28ac773f74ba00ed1f312572435',
      '000000000000000000000000000000000000000000000000',
      'GCM Test Case 7',
      dict(mode='GCM', nonce='000000000000000000000000')
    ),

    ( '|00000000000000000000000000000000',
      '|98e7247c07f0fe411c267e4384b0f600|2ff58d80033927ab8ef4d4587514f0fb',
      '000000000000000000000000000000000000000000000000',
      'GCM Test Case 8',
      dict(mode='GCM', nonce='000000000000000000000000')
    ),

    ( '|d9313225f88406e5a55909c5aff5269a86a7a9531534f7da2e4c303d8a318a72' +
       '1c3c0c95956809532fcf0e2449a6b525b16aedf5aa0de657ba637b391aafd255',
      '|3980ca0b3c00e841eb06fac4872a2757859e1ceaa6efd984628593b40ca1e19c'  +
       '7d773d00c144c525ac619d18c84a3f4718e2448b2fe324d9ccda2710acade256|' +
       '9924a7c8587336bfb118024db8674a14',
      'feffe9928665731c6d6a8f9467308308feffe9928665731c',
      'GCM Test Case 9',
      dict(mode='GCM', nonce='cafebabefacedbaddecaf888')
    ),

    ( 'feedfacedeadbeeffeedfacedeadbeefabaddad2|' +
      'd9313225f88406e5a55909c5aff5269a86a7a9531534f7da2e4c303d8a318a72' +
      '1c3c0c95956809532fcf0e2449a6b525b16aedf5aa0de657ba637b39',
      'feedfacedeadbeeffeedfacedeadbeefabaddad2|' +
      '3980ca0b3c00e841eb06fac4872a2757859e1ceaa6efd984628593b40ca1e19c'  +
      '7d773d00c144c525ac619d18c84a3f4718e2448b2fe324d9ccda2710|' +
      '2519498e80f1478f37ba55bd6d27618c',
      'feffe9928665731c6d6a8f9467308308feffe9928665731c',
      'GCM Test Case 10',
      dict(mode='GCM', nonce='cafebabefacedbaddecaf888')
    ),

    ( 'feedfacedeadbeeffeedfacedeadbeefabaddad2|' +
      'd9313225f88406e5a55909c5aff5269a86a7a9531534f7da2e4c303d8a318a72' +
      '1c3c0c95956809532fcf0e2449a6b525b16aedf5aa0de657ba637b39',
      'feedfacedeadbeeffeedfacedeadbeefabaddad2|' +
      '0f10f599ae14a154ed24b36e25324db8c566632ef2bbb34f8347280fc4507057' +
      'fddc29df9a471f75c66541d4d4dad1c9e93a19a58e8b473fa0f062f7|' +
      '65dcc57fcf623a24094fcca40d3533f8',
      'feffe9928665731c6d6a8f9467308308feffe9928665731c',
      'GCM Test Case 11',
      dict(mode='GCM', nonce='cafebabefacedbad')
    ),

    ( 'feedfacedeadbeeffeedfacedeadbeefabaddad2|' +
      'd9313225f88406e5a55909c5aff5269a86a7a9531534f7da2e4c303d8a318a72' +
      '1c3c0c95956809532fcf0e2449a6b525b16aedf5aa0de657ba637b39',
      'feedfacedeadbeeffeedfacedeadbeefabaddad2|' +
      'd27e88681ce3243c4830165a8fdcf9ff1de9a1d8e6b447ef6ef7b79828666e45' +
      '81e79012af34ddd9e2f037589b292db3e67c036745fa22e7e9b7373b|' +
      'dcf566ff291c25bbb8568fc3d376a6d9',
      'feffe9928665731c6d6a8f9467308308feffe9928665731c',
      'GCM Test Case 12',
      dict(mode='GCM', nonce='9313225df88406e555909c5aff5269aa'+
          '6a7a9538534f7da1e4c303d2a318a728c3c0c95156809539fcf0e2429a6b5254'+
          '16aedbf5a0de6a57a637b39b' )
    ),

    ( '|',
      '||530f8afbc74536b9a963b4f1c4cb738b',
      '0000000000000000000000000000000000000000000000000000000000000000',
      'GCM Test Case 13',
      dict(mode='GCM', nonce='000000000000000000000000')
    ),

    ( '|00000000000000000000000000000000',
      '|cea7403d4d606b6e074ec5d3baf39d18|d0d1c8a799996bf0265b98b5d48ab919',
      '0000000000000000000000000000000000000000000000000000000000000000',
      'GCM Test Case 14',
      dict(mode='GCM', nonce='000000000000000000000000')
    ),

    ( '|d9313225f88406e5a55909c5aff5269a86a7a9531534f7da2e4c303d8a318a72' +
       '1c3c0c95956809532fcf0e2449a6b525b16aedf5aa0de657ba637b391aafd255',
      '|522dc1f099567d07f47f37a32a84427d643a8cdcbfe5c0c97598a2bd2555d1aa'  +
       '8cb08e48590dbb3da7b08b1056828838c5f61e6393ba7a0abcc9f662898015ad|' +
       'b094dac5d93471bdec1a502270e3cc6c',
      'feffe9928665731c6d6a8f9467308308feffe9928665731c6d6a8f9467308308',
      'GCM Test Case 15',
      dict(mode='GCM', nonce='cafebabefacedbaddecaf888')
    ),

    ( 'feedfacedeadbeeffeedfacedeadbeefabaddad2|' +
      'd9313225f88406e5a55909c5aff5269a86a7a9531534f7da2e4c303d8a318a72' +
      '1c3c0c95956809532fcf0e2449a6b525b16aedf5aa0de657ba637b39',
      'feedfacedeadbeeffeedfacedeadbeefabaddad2|' +
      '522dc1f099567d07f47f37a32a84427d643a8cdcbfe5c0c97598a2bd2555d1aa'  +
      '8cb08e48590dbb3da7b08b1056828838c5f61e6393ba7a0abcc9f662|' +
      '76fc6ece0f4e1768cddf8853bb2d551b',
      'feffe9928665731c6d6a8f9467308308feffe9928665731c6d6a8f9467308308',
      'GCM Test Case 16',
      dict(mode='GCM', nonce='cafebabefacedbaddecaf888')
    ),

    ( 'feedfacedeadbeeffeedfacedeadbeefabaddad2|' +
      'd9313225f88406e5a55909c5aff5269a86a7a9531534f7da2e4c303d8a318a72' +
      '1c3c0c95956809532fcf0e2449a6b525b16aedf5aa0de657ba637b39',
      'feedfacedeadbeeffeedfacedeadbeefabaddad2|' +
      'c3762df1ca787d32ae47c13bf19844cbaf1ae14d0b976afac52ff7d79bba9de0' +
      'feb582d33934a4f0954cc2363bc73f7862ac430e64abe499f47c9b1f|' +
      '3a337dbf46a792c45e454913fe2ea8f2',
      'feffe9928665731c6d6a8f9467308308feffe9928665731c6d6a8f9467308308',
      'GCM Test Case 17',
      dict(mode='GCM', nonce='cafebabefacedbad')
    ),

    ( 'feedfacedeadbeeffeedfacedeadbeefabaddad2|' +
      'd9313225f88406e5a55909c5aff5269a86a7a9531534f7da2e4c303d8a318a72' +
      '1c3c0c95956809532fcf0e2449a6b525b16aedf5aa0de657ba637b39',
      'feedfacedeadbeeffeedfacedeadbeefabaddad2|' +
      '5a8def2f0c9e53f1f75d7853659e2a20eeb2b22aafde6419a058ab4f6f746bf4' +
      '0fc0c3b780f244452da3ebf1c5d82cdea2418997200ef82e44ae7e3f|' +
      'a44a8266ee1c8eb0c8b5d4cf5ae9f19a',
      'feffe9928665731c6d6a8f9467308308feffe9928665731c6d6a8f9467308308',
      'GCM Test Case 18',
      dict(mode='GCM', nonce='9313225df88406e555909c5aff5269aa'+
          '6a7a9538534f7da1e4c303d2a318a728c3c0c95156809539fcf0e2429a6b5254'+
          '16aedbf5a0de6a57a637b39b' )
    ),
]

def get_tests(config={}):
    from Crypto.Cipher import AES
    from Crypto.Util import cpuid
    from common import make_block_tests

    tests = make_block_tests(AES, "AES", test_data, {'use_aesni': False})
    if cpuid.have_aes_ni():
        # Run tests with AES-NI instructions if they are available.
        tests += make_block_tests(AES, "AESNI", test_data, {'use_aesni': True})
    return tests

if __name__ == '__main__':
    import unittest
    suite = lambda: unittest.TestSuite(get_tests())
    unittest.main(defaultTest='suite')

# vim:set ts=4 sw=4 sts=4 expandtab:
