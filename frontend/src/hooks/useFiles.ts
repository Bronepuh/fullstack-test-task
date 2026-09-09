import { useCallback, useEffect, useState } from "react";
import { AlertItem, FileItem } from "../types";
import { fetchAlerts, fetchFiles, uploadFileAPI } from "../api/client";

export function useFiles() {
	const [files, setFiles] = useState<FileItem[]>([]);
	const [alerts, setAlerts] = useState<AlertItem[]>([]);
	const [isLoading, setIsLoading] = useState(true);
	const [isSubmitting, setIsSubmitting] = useState(false);
	const [errorMessage, setErrorMessage] = useState<string | null>(null);

	const loadData = useCallback(async () => {
		setIsLoading(true);
		setErrorMessage(null);
		try {
			const [filesData, alertsData] = await Promise.all([fetchFiles(), fetchAlerts()]);
			setFiles(filesData);
			setAlerts(alertsData);
		} catch (error) {
			setErrorMessage(error instanceof Error ? error.message : "Ошибка загрузки");
		} finally {
			setIsLoading(false);
		}
	}, []);

	useEffect(() => {
		void loadData();
	}, [loadData]);

	const handleUpload = async (title: string, file: File): Promise<boolean> => {
		setIsSubmitting(true);
		setErrorMessage(null);
		try {
			await uploadFileAPI(title, file);
			await loadData();
			return true; // Возвращаем true, чтобы модалка знала, что пора закрываться
		} catch (error) {
			setErrorMessage(error instanceof Error ? error.message : "Ошибка загрузки");
			return false;
		} finally {
			setIsSubmitting(false);
		}
	};

	return {
		files,
		alerts,
		isLoading,
		isSubmitting,
		errorMessage,
		loadData,
		handleUpload,
	};
}
