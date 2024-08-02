# pytest-order-iota

This is just an inspiration of how to automate [`pytest`](https://pypi.org/project/pytest/) ordering via [`pytest-order`](https://pypi.org/project/pytest-order/).

Of course this also works with everything else requiring `iota`, it's not just limited to `pytest` and `pytest-order`. Test ordering is just the only use case I find the concept of `iota` very useful at the moment.

It's also here so I don't forget how it works.

## iota?!

An ever-incrementing integer value, basically.

I got the name from Go (https://go.dev/wiki/Iota), but in C++ for example there's also `std::iota` (https://en.cppreference.com/w/cpp/algorithm/iota).

## Why?

Useful if you have a bunch of tests written with a specific order in mind, but at some point you're faced with the problem of re-ordering your tests.

Example:

```python
@pytest.mark.order(0)
def test_component_a:
    ...


@pytest.mark.order(1)
def test_component_b:
    ...


@pytest.mark.order(2)
def test_component_c:
    ...
```

Test order:
```
test_component_a = 0
test_component_b = 1
test_component_c = 2
```

Assuming your production code has changed, and you now have a hypothetical component `z`, and the test for that component has to be executed before component `c`. Okay, so you go ahead and add it between `test_component_b` and `test_component_c`, but because the testing boilerplate is always the same, you resort to good old copy and paste of `test_component_c`:

```python
@pytest.mark.order(0)
def test_component_a:
    ...


@pytest.mark.order(1)
def test_component_b:
    ...


# Test for component Z added
@pytest.mark.order(2)
def test_component_z:
    ...


@pytest.mark.order(2)
def test_component_c:
    ...
```

Because of copy-pasting, the order of `test_component_z` and `test_component_c` is the same, so they're either executed in parallel, or we simply don't know which order `pytest-order` chooses.

The test order is now:
```
test_component_a = 0
test_component_b = 1
test_component_z = 2   <--- correct
test_component_c = 2   <--- wrong, should be 3
```

Now, let's refactor the original example with `iota` from [`pytest-order-iota.py`](pytest-order-iota.py):

```python
@pytest.mark.order(iota())
def test_component_a:
    ...


@pytest.mark.order(iota())
def test_component_b:
    ...


@pytest.mark.order(iota())
def test_component_c:
    ...
```

Test order:
```
test_component_a = 0
test_component_b = 1
test_component_c = 2
```

And with `test_component_z` added (meaning, the boilerplate code copy-pasted from `test_component_c`):
```python
@pytest.mark.order(iota())
def test_component_a:
    ...


@pytest.mark.order(iota())
def test_component_b:
    ...


# Test for component Z added
@pytest.mark.order(iota())
def test_component_z:
    ...


@pytest.mark.order(iota())
def test_component_c:
    ...
```

The test order is now:
```
test_component_a = 0
test_component_b = 1
test_component_z = 2   <--- correct
test_component_c = 3   <--- correct
```

... without manually changing the value for the `@pytest.mark.order` decorator.
