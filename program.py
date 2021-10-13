import fileinput

#s boxes
s0 = {
  ('00','00'): '01', ('00','01'): '00', ('00','10'): '11', ('00','11'): '10',
  ('01','00'): '11', ('01','01'): '10', ('01','10'): '01', ('01','11'): '00',
  ('10','00'): '00', ('10','01'): '10', ('10','10'): '01', ('10','11'): '11',
  ('11','00'): '11', ('11','01'): '01', ('11','10'): '11', ('11','11'): '10'
}

s1 = {
  ('00','00'): '00', ('00','01'): '01', ('00','10'): '10', ('00','11'): '11',
  ('01','00'): '10', ('01','01'): '00', ('01','10'): '01', ('01','11'): '11',
  ('10','00'): '11', ('10','01'): '00', ('10','10'): '01', ('10','11'): '00',
  ('11','00'): '10', ('11','01'): '01', ('11','10'): '00', ('11','11'): '11'
}

#permutations
def permutation(input, permutations):
  tmp = [i for i in input]
  for i in range(len(tmp)):
    tmp[i] = input[permutations[i]]
  string = ''
  return string.join(tmp)

#subkeys
def subkeys(key):
  permuted = permutation(key, (2,4,1,6,3,9,0,8,7,5))
  part1 = permuted[:5]
  part2 = permuted[5:]
  part1 = rotate_left(part1, 1)
  part2 = rotate_left(part2, 1)
  key1 = extract_parts(part1+part2, (5,2,6,3,7,4,9,8))
  part1 = rotate_left(part1, 2)
  part2 = rotate_left(part2, 2)
  key2 = extract_parts(part1+part2, (5,2,6,3,7,4,9,8))
  return (key1, key2)

def rotate_left(s, d):
  tmp = s[d : ] + s[0 : d]
  return tmp

def extract_parts(string, parts):
  tmp = ''
  for x in parts:
    tmp = tmp + string[x]
  return tmp

#xor 
def xor(x, y):
  res = ''
  for i in range(len(x)):
    tmp = int(x[i]) ^ int(y[i])
    res = res + str(tmp)
  return res


def feistel(half, subkey):
  expanded = extract_parts(half, (3,0,1,2,1,2,3,0))
  expanded = xor(expanded, subkey)
  part1 = expanded[:4]
  part2 = expanded[4:]
  coords0 = (part1[0] + part1[3], part1[1] + part1[2])
  coords1 = (part2[0] + part2[3], part2[1] + part2[2])
  res = s0[coords0] + s1[coords1]
  res = permutation(res, (1,3,2,0))
  return res

# encrypt
plaintext = ''
key = ''
action = ''
count = 0
# Recibe la entrada
for line in fileinput.input():
  if count == 0:
    action = line
    count += 1
    continue
  if count == 1:
    key = line
    count += 1
    continue
  if count == 2:
    plaintext = line
    break
plaintext = plaintext.replace('\n', '')
key = key.replace('\n', '')
action = action.replace('\n', '')

if action == 'E':
  subkey1, subkey2 = subkeys(key)
  # initial permutation
  permuted_text = permutation(plaintext, (1,5,2,0,3,7,4,6))
  # mixing
  right_half = permuted_text[:4]
  left_half = permuted_text[4:]
  new_half1 = feistel(left_half, subkey1)
  new_half1 = xor(new_half1, right_half)
  # interchange
  text_interchanged = left_half + new_half1
  # mixing
  right_half = text_interchanged[4:]
  left_half = text_interchanged[:4]
  new_half2 = feistel(right_half, subkey2)
  new_half2 = xor(new_half2, left_half)
  # concatenate
  result = new_half2 + new_half1
  # reverse permutation
  result = permutation(result, (3,0,2,4,6,1,7,5))
  print(result)
else:
  subkey1, subkey2 = subkeys(key)
  # initial permutation
  permuted_text = permutation(plaintext, (1,5,2,0,3,7,4,6))
  # mixing
  right_half = permuted_text[:4]
  left_half = permuted_text[4:]
  new_half1 = feistel(left_half, subkey2)
  new_half1 = xor(new_half1, right_half)
  # interchange
  text_interchanged = left_half + new_half1
  # mixing
  right_half = text_interchanged[4:]
  left_half = text_interchanged[:4]
  new_half2 = feistel(right_half, subkey1)
  new_half2 = xor(new_half2, left_half)
  # concatenate
  result = new_half2 + new_half1
  # reverse permutation
  result = permutation(result, (3,0,2,4,6,1,7,5))
  print(result)