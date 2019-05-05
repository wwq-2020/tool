# quick start
pipenv --python python2.7
pipenv shell
pipenv install

run:
python gotool.py j2s '{"test":1}'

got: 
type tmp struct {
	Test int64 `json:"test"`
}
