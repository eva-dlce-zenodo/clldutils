
Releasing clldutils
===================

Clone `clld/clldutils` and switch to the `master` branch. Then:

- Do platform test via ``tox`` (making sure statement coverage is at 100%):
```shell
tox -r
```

- Make sure ``flake8`` passes (configuration in ``setup.cfg``):
```shell
flake8 src/clldutils
```

- Make sure the docs render:
  ```shell
  cd docs
  make clean html
  cd ..
  ```

- Change version to the new version number in
  - `setup.py`
  - `src/clldutils/__init__.py`
  - `docs/conf.py`
  - `CHANGES.md`

- Commit your change of the version number:
```shell
git commit -a -m "release <VERSION>"
```

- Create a release tag:
```shell
git tag -a v<VERSION> -m "<VERSION> release"
```

- Release to PyPI:
```shell
python setup.py clean --all
rm dist/*
python setup.py sdist bdist_wheel
twine upload dist/*
```

- Push to GitHub:
```shell
git push origin
git push --tags origin
```

- Increment the version number and append `.dev0` to start the new development cycle:
  - `src/clldutils/__init__.py`
  - `setup.py`
  - `docs/conf.py`

- Commit/push the version change:
```shell
git commit -a -m "bump version for development"
git push origin
```
