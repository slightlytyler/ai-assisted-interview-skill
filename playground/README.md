# splitter

Shared expense ledger. See `SPEC.md` for what to build.

## Running and testing

Requires Python 3.11+. No dependencies to install.

```sh
python3 -m unittest -v                                            # all tests
python3 -m unittest tests.test_models -v                          # one file
python3 -m unittest tests.test_models.GroupTest.test_add_member   # one test
```

Try it from a REPL:

```sh
python3 -c "from splitter import Group; g = Group('offsite'); g.add_member('alice'); print(g.members)"
```
