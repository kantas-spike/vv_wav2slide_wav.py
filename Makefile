DST_DIR=${HOME}/bin
SCRIPT_HOME=$(dir $(abspath vv_wav2slide_wav.py))


vv_wav2slide_wav.sh: vv_wav2slide_wav.sh.tmpl
	cat vv_wav2slide_wav.sh.tmpl | sed -e 's#@@@SCRIPT_HOME_DIR@@@#${SCRIPT_HOME}#' > $@

clean: vv_wav2slide_wav.sh
	rm $^

install: vv_wav2slide_wav.sh
	mkdir -p ${DST_DIR}
	cp $< ${DST_DIR}
	chmod u+x ${DST_DIR}/$<