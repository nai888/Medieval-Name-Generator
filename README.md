# Medieval Name Generator
A python CLI that generates randomized medieval English names.

## Name Generator

To run the generator:

```bash
python3 mng.py
```

This will output 5 fully random names, male and female, commoner and noble. E.g.:

```txt
Wynhelm Tilwick
Everwin Warkmere
Aedelthryth Alfredett
Hildewine Fulkeett
Amicia Tristham
```

Indicate how many results you want by adding a number to the command:

```bash
python3 mng.py 10
```

Other arguments include:

- `--male` for only male given names,
- `--female` for only female given names,
- `--commoner` for only commoner surnames,
- `--noble` for only noble surnames,
- `--unique-last` to only allow each surname once,
- `--unique-full` to only allow each combination of given and surname once,
- `--seed INT` to set the seed of the randomization for repeatable output where INT is an integer,
- `--out FILE` to write newline-separated names to the text file set by FILE,
- `--csv FILE` to write names to the CSV file set by FILE,
- `--no-stdout` to stop the program from printing out the names, used in combination with either of the prior two commands, and
- `-h` or `--help` to show a help file.

For example, the following command will generate 10 unique noble male names and save them to a text file named `./output/names.txt`, but will not print the output to the terminal:

```bash
python3 mng.py 10 --noble --male --unique-full --out ./output/names.txt --no-stdout --seed 5
```

Further, since `--seed 5` was included, the output of the above command will *always* be:

```txt
Yrmenfrith Fellwall
Hrothwine Tudorley
Sigefrid Blackstone
Osmwald Tilmoor
Godfrith Sandridge
Aubry Winterstoke
Derwin Chargrove
Ivo Longford
Godbeald Henleystone
Sigmaer Cartstone
```

## List Output

Alternatively, to just output an entire list in a space-separated text file, use the `mng-list.py` file instead.

- `--list mfirst` will output the entire list of male first names,
- `--list ffirst` will output the entire list of female first names,
- `--list clast` will output the entire list of commoner last names, and
- `--list nlast` will output the entire list of noble last names.

For example:

```bash
python3 mng-list.py --list ffirst --out ./output/ffirst.txt
```

The above command will output the entirety of the female first name list separated by spaces in a text file named `./output/ffirst.txt`.
